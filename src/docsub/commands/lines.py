import re
from typing import Any, Iterable, Self, override

from ..__base__ import Substitution, Line, Location, Modifier


N = r'[1-9][0-9]*'
RX_LINES = re.compile(
    rf'^(?:\s*after\s+(?P<first>{N}))?(?:\s*upto\s+-(?P<last>{N}))?\s*$'
)


class LinesCommand(Modifier, name='lines'):
    def __init__(self, first: int, last: int, loc: Location):
        super().__init__(loc)
        self.first = first
        self.last = last
        self.first_lines: list[Line] = []
        self.last_lines: list[Line] = []
        self.is_empty = True

    @override
    @classmethod
    def parse_args(cls, args: str, *, conf: Any = None, loc: Location) -> Self:
        if not args.strip():
            raise cls.error_invalid_args(args, loc=loc)
        if not (match := RX_LINES.match(args)):
            raise cls.error_invalid_args(args, loc=loc)
        return cls(
            first=int(match.group('first') or 0),
            last=int(match.group('last') or 0),
            loc=loc,
        )

    @override
    def on_content_line(self, line: Line, ctx: Substitution) -> None:
        is_first_full = self.first == len(self.first_lines)
        is_last_full = self.last == len(self.last_lines)
        if not is_first_full:
            self.first_lines.append(line)  # store line from initial range
        elif not is_last_full:
            self.last_lines.append(line)  # store line that can be in trailing range
        elif self.last > 0:
            # update possible trailing range
            self.last_lines.pop(0)
            self.last_lines.append(line)
        elif self.last == 0:
            pass  # no need to update trailing range
        else:
            raise AssertionError('unreachable')

    @override
    def before_producers(self, ctx: Substitution) -> Iterable[Line]:
        yield from self.first_lines

    @override
    def after_producers(self, ctx: Substitution) -> Iterable[Line]:
        yield from self.last_lines
