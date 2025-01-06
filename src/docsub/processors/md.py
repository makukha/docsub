from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Self, override

from ..__base__ import Substitution, InvalidSubstitution, Line, Location, StopSubstitution
from ..commands import command
from ..config import DocsubConfig


PREFIX = r'^\s*<!--\s*docsub:'

RX_DOCSUB = re.compile(PREFIX)
RX_BEGIN = re.compile(PREFIX + r'\s*begin(?:\s+#(?P<id>\S+))?\s*-->\s*$')
RX_END = re.compile(PREFIX + r'\s*end(?:\s+#(?P<id>\S+))?\s*-->\s*$')
RX_COMMAND = re.compile(PREFIX + fr'\s*(?P<name>{'|'.join(command)})(\s+(?P<args>\S.*))?\s*-->\s*')


@dataclass
class BlockSubstitution(Substitution):
    conf: DocsubConfig
    all_commands_consumed: bool = False

    @override
    @classmethod
    def match(cls, line: Line, conf: DocsubConfig) -> Self | None:
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
        if m := RX_COMMAND.match(line.text):
            name = m.group('name')
            conf = getattr(self.conf.command, name, None)
            cmd = command[name].parse_args(m.group('args'), conf=conf, loc=line.loc)
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
                loc=self.loc
            )


class MarkdownProcessor:
    def __init__(self, conf: DocsubConfig):
        self.conf = conf

    def process_document(self, file: Path) -> Iterable[str]:
        block: BlockSubstitution | None = None

        with file.open('rt') as f:
            lineno = 0
            while text := f.readline():
                line = Line(text=text, loc=Location(fname=file, lineno=lineno))
                if not block:
                    # block begins?
                    if (block := BlockSubstitution.match(line, conf=self.conf)):
                        block.conf = self.conf
                    yield line.text  # yield plain line or block header
                else:
                    # let block process line
                    try:
                        yield from (ln.text for ln in block.consume_line(line))
                    except StopSubstitution:
                        del block
                        block = None
                lineno += 1
