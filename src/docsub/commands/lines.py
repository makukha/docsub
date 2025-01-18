import re
from typing import Iterable, override

from ..__base__ import Substitution, Line, Location, Modifier


N = r'[1-9][0-9]*'
RX_LINES = re.compile(
    rf'^(?:\s*after\s+(?P<first>{N}))?(?:\s*upto\s+-(?P<last>{N}))?\s*$'
)


class LinesCommand(Modifier, name='lines'):
    def __init__(self, args: str, *, loc: Location, **kw) -> None:
        super().__init__(args, loc=loc)
        if not args.strip():
            raise self.exc_invalid_args()
        if not (match := RX_LINES.match(args)):
            raise self.exc_invalid_args()
        self.first = int(match.group('first') or 0)
        self.last = int(match.group('last') or 0)
        self.first_lines: list[Line] = []
        self.last_lines: list[Line] = []
        self.is_empty = True

    @override
    def on_content_line(self, line: Line, sub: Substitution) -> None:
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
    def before_producers(self, sub: Substitution) -> Iterable[Line]:
        yield from self.first_lines

    @override
    def after_producers(self, sub: Substitution) -> Iterable[Line]:
        yield from self.last_lines
