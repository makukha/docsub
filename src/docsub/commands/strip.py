from typing import Any, Iterable, Self, override

from ..__base__ import Substitution, Line, Location, Modifier


class StripCommand(Modifier, name='strip'):
    def __init__(self, loc: Location):
        super().__init__(loc)
        self.lines: list[Line] = []
        self.is_empty = True

    @override
    @classmethod
    def parse_args(cls, args: str, *, conf: Any = None, loc: Location) -> Self:
        if args.strip():
            raise cls.error_invalid_args(args, loc=loc)
        return cls(loc)

    @override
    def on_produced_line(self, line: Line, ctx: Substitution) -> Iterable[Line]:
        line.text = line.text.strip() + '\n'
        if self.is_empty:
            if line.text:  # first non-blank line
                self.is_empty = False
                yield line
            else:
                pass  # blank line suppressed
        else:
            if line.text:  # some non-empty line
                while self.lines:  # yield from lines buffer
                    yield self.lines.pop()
            else:
                self.lines.append(line)  # empty line may be trailing, push to buffer
                # empty lines from buffer will never be returned if iteration stops
