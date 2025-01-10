from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Self, override

from ..__base__ import (
    Substitution,
    InvalidSubstitution,
    Line,
    Location,
    StopSubstitution,
    SyntaxElement,
)
from ..commands import COMMANDS
from ..config import DocsubSettings


RX_FENCE = re.compile(r'^(?P<indent>\s*)(?P<fence>```+|~~~+).*$')

DOCSUB_PREFIX = r'^\s*<!--\s*docsub:'
RX_DOCSUB = re.compile(DOCSUB_PREFIX)
RX_BEGIN = re.compile(DOCSUB_PREFIX + r'\s*begin(?:\s+#(?P<id>\S+))?\s*-->\s*$')
RX_END = re.compile(DOCSUB_PREFIX + r'\s*end(?:\s+#(?P<id>\S+))?\s*-->\s*$')
RX_CMD = re.compile(
    DOCSUB_PREFIX + rf'\s*(?P<name>{"|".join(COMMANDS)})(\s+(?P<args>\S.*))?\s*-->\s*'
)


@dataclass
class BlockSubstitution(Substitution):
    conf: DocsubSettings
    all_commands_consumed: bool = False

    @override
    @classmethod
    def match(cls, line: Line, conf: DocsubSettings) -> Self | None:
        if not RX_DOCSUB.match(line.text):
            return None
        if not (match := RX_BEGIN.match(line.text)):
            raise cls.error_invalid(line.text, loc=line.loc)
        return cls(loc=line.loc, id=match.group('id') or None, conf=conf)

    @override
    def consume_line(self, line: Line) -> Iterable[Line]:
        # block end?
        if m := RX_END.match(line.text):
            if (m.group('id') or None) == self.id:  # end of this block
                self.validate_assumptions()
                yield from self.produce_lines()
                yield line
                raise StopSubstitution
            else:  # plain line, end of another block
                self.all_commands_consumed = True  # maybe it was first after commands
                self.validate_assumptions()
                # process this line below

        # plain line because all commands consumed?
        if self.all_commands_consumed:
            self.process_content_line(line)
            return

        # command?
        if m := RX_CMD.match(line.text):
            name = m.group('name')
            conf = getattr(self.conf.command, name, None)
            cmd = COMMANDS[name].parse_args(
                args=m.group('args') or '',
                conf=conf,
                loc=line.loc,
            )
            self.append_command(cmd)
            yield line
            return

        # plain line, first after commands
        self.all_commands_consumed = True
        self.validate_assumptions()
        self.process_content_line(line)
        return

    def validate_assumptions(self) -> None:
        """
        Validate block assumptions.
        """
        if not len(self.producers):
            raise InvalidSubstitution(
                'Block must contain producing command',
                loc=self.loc,
            )


@dataclass
class Fence(SyntaxElement):
    indent: str
    fence: str

    @classmethod
    def match(cls, line: Line) -> Self | None:
        if match := RX_FENCE.match(line.text):
            return cls(**match.groupdict(), loc=line.loc)
        return None

    def match_end(self, line: Line) -> bool:
        if other := self.match(line):
            return self.indent == other.indent and self.fence == other.fence
        return False


class MarkdownProcessor:
    def __init__(self, conf: DocsubSettings):
        self.conf = conf

    def process_document(self, file: Path) -> Iterable[str]:
        block: BlockSubstitution | None = None
        fences: list[Fence] = []

        with file.open('rt') as f:
            lineno = 0
            while text := f.readline():
                line = Line(text=text, loc=Location(fname=file, lineno=lineno))

                # delegate line processing to block
                if block:
                    try:
                        yield from (ln.text for ln in block.consume_line(line))
                    except StopSubstitution:
                        block = None

                # inside fenced code block, all lines are plain
                elif fences:
                    yield line.text
                    if fences[-1].match_end(line):  # end of fenced code block
                        fences.pop()
                    elif fence := Fence.match(line):  # nested fenced code block
                        fences.append(fence)

                # block begins?
                elif block := BlockSubstitution.match(line, conf=self.conf):
                    yield line.text
                    block.conf = self.conf

                # top level fenced code block?
                elif fence := Fence.match(line):
                    yield line.text
                    fences.append(fence)

                # just a plain line
                else:
                    yield line.text  # yield plain line or block header

                lineno += 1
