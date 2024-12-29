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

    _RX: ClassVar[re.Pattern]

    @classmethod
    def from_line(cls, line: str, loc: Location) -> Self | None:
        line = line.rstrip()  # remove trailing newline
        if match := cls._RX.fullmatch(line):
            return cls(**match.groupdict(), loc=loc)


@dataclass
class Substitution(SyntaxElement):
    stmt: str
    cmd: BaseCommand | None = None
    content: Any | None = None

    _RX = re.compile(r'^\s*<!--\s*docsub:\s+(?P<stmt>.+\S)\s*-->\s*$')


@dataclass
class Fence(SyntaxElement):
    loc: Location
    indent: str
    fence: str

    _RX = re.compile(r'^(?P<indent>\s*)(?P<fence>```+).*$')

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
                    yield line
                    try:
                        yield from add_ending_newline(sub.cmd.generate_lines())
                    except DocsubError as exc:
                        exc.loc = loc
                        raise exc
                    continue
                else:
                    raise DocsubError('Invalid docsub substitution block', loc=loc)

            elif sub and sub.content:
                # check for block closing
                if (end := Fence.from_line(line, loc=loc)) and end.match(sub.content):
                    yield line
                    sub = None
                    continue
                # otherwise suppress line
                continue

            else:
                assert_never(sub)
