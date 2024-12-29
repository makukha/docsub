from collections.abc import Iterable
from dataclasses import astuple, dataclass
from pathlib import Path
import re
from typing import Self

from ..commands import BaseCommand, parse_command
from ..config import Config
from ..errors import Location, DocsubError
from ..util import add_ending_newline


RX_FENCE = re.compile(
    r'(?P<indent>\s*)(?P<fence>```+)\s*(?P<syntax>((?!@docsub:)\S)+)?'
    r'(?:\s*@docsub:\s*(?P<statement>.*)|.*)',
    flags=re.DOTALL,
)


@dataclass(kw_only=True)
class Scope:
    command: BaseCommand | None = None


@dataclass
class FencedScope(Scope):
    loc: Location
    indent: str
    fence: str
    syntax: str
    statement: str

    def __post_init__(self):
        self.loc = Location(*astuple(self.loc))

    @classmethod
    def from_line(cls, line: str, loc: Location) -> Self | None:
        if match := RX_FENCE.fullmatch(line.rstrip()):  # remove trailing newline
            return cls(**match.groupdict(), loc=loc)

    def match(self, other: Self) -> bool:
        if not isinstance(other, FencedScope):
            return False
        return (self.indent, self.fence) == (other.indent, other.fence)


def process_md_document(file: Path, *, conf: Config) -> Iterable[str]:
    scopes = [Scope()]  # root scope for readable code
    with file.open('rt') as f:
        loc = Location(file, lineno=0)
        while line := f.readline():
            loc.lineno += 1
            fence = FencedScope.from_line(line, loc=loc)

            # closing fence
            if fence and fence.match(scopes[-1]):
                current = scopes.pop()
                if current.command or not any(s.command for s in scopes):
                    yield line

            # new fence
            elif fence and not any(f.command for f in scopes):
                scopes.append(fence)
                yield line
                try:
                    if fence.statement:  # docsub statement found
                        fence.command = parse_command(fence.statement, conf.command)
                        yield from add_ending_newline(fence.command.generate_lines())
                except DocsubError as exc:
                    exc.loc = loc
                    raise exc

            # plain line
            else:
                if not any(f.command for f in scopes):
                    yield line
