from collections.abc import Iterable
from copy import copy
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, ClassVar, Self, assert_never

from ..commands import BaseCommand, parse_command
from ..config import Config
from ..errors import Location, DocsubError
from ..util import add_ending_newline


@dataclass
class SyntaxElement:
    loc: Location

    def __post_init__(self):
        self.loc = copy(self.loc)


@dataclass(kw_only=True)
class Substitution(SyntaxElement):
    args: str
    after_line: int | None = None
    # command
    stmt: str
    cmd: BaseCommand | None = None
    # runtime
    content: Any | None = None
    lines_kept: int | None = None

    def __post_init__(self):
        if self.after_line is not None:
            self.after_line = int(self.after_line)

    _R_PREFIX = r'^\s*<!--\s*docsub\b'
    _R_ARGS = r'after\s+line\s+(?P<after_line>[1-9][0-9]*)'
    _RX_PREFIX = re.compile(_R_PREFIX)
    _RX_HEADER = re.compile(
        fr'{_R_PREFIX}(?P<args>\s+{_R_ARGS}\s*)?:\s+(?P<stmt>.+\S)\s*-->\s*$'
    )

    @classmethod
    def from_line(cls, line: str, loc: Location) -> Self | None:
        line = line.rstrip()  # remove trailing newline
        if cls._RX_PREFIX.match(line):
            if not (match := cls._RX_HEADER.fullmatch(line)):
                raise DocsubError(f'Invalid docsub header: {line}')
            else:
                return cls(**match.groupdict(), loc=loc)


@dataclass
class Fence(SyntaxElement):
    loc: Location
    indent: str
    fence: str

    _RX = re.compile(r'^(?P<indent>\s*)(?P<fence>```+).*$')

    @classmethod
    def from_line(cls, line: str, loc: Location) -> Self | None:
        line = line.rstrip()  # remove trailing newline
        if match := cls._RX.fullmatch(line):
            return cls(**match.groupdict(), loc=loc)

    def match(self, other: Self) -> bool:
        return (
            isinstance(other, Fence)
            and (self.indent, self.fence) == (other.indent, other.fence)
        )


def process_md_document(file: Path, *, conf: Config) -> Iterable[str]:
    sub: Substitution | None = None

    with file.open('rt') as f:
        loc = Location(file, lineno=0)
        while line := f.readline():
            loc.lineno += 1

            if not sub:
                # expect sub header or plain line
                if sub := Substitution.from_line(line, loc):
                    yield line
                    try:
                        sub.cmd = parse_command(sub.stmt, conf.command)
                    except DocsubError as exc:
                        exc.loc = loc
                        raise exc
                    continue
                else:
                    yield line
                    continue

            elif sub and not sub.content:
                # expect content block
                if content := Fence.from_line(line, loc=loc):
                    sub.content = content
                    if sub.after_line:
                        sub.lines_kept = 0
                    yield line
                else:
                    raise DocsubError('Invalid docsub substitution block', loc=loc)

            elif sub and sub.content:
                # check for block closing
                if (end := Fence.from_line(line, loc=loc)) and end.match(sub.content):
                    try:
                        yield from add_ending_newline(sub.cmd.generate_lines())
                    except DocsubError as exc:
                        exc.loc = loc
                        raise exc
                    yield line
                    sub = None
                    continue

                # keep line, if needed
                elif sub.after_line and sub.lines_kept < sub.after_line:
                    yield line
                    sub.lines_kept += 1
                    continue

                # otherwise suppress line
                else:
                    continue

            else:
                assert_never(sub)
