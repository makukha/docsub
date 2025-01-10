from typing import Any, Iterable, Self, override

from ..__base__ import Substitution, Line, Location, Modifier


class StripCommand(Modifier, name='strip'):
    def __init__(self, loc: Location):
        super().__init__(loc)
        self.lines: list[Line] = []
        self.saw_non_empty = False

    @override
    @classmethod
    def parse_args(cls, args: str, *, conf: Any = None, loc: Location) -> Self:
        if args.strip():
            raise cls.error_invalid_args(args, loc=loc)
        return cls(loc)

    @override
    def on_produced_line(self, line: Line, ctx: Substitution) -> Iterable[Line]:
        line.text = line.text.strip() + '\n'

        if line.text.isspace():
            if self.saw_non_empty:
                self.lines.append(line)  # empty line may be trailing, push to buffer
            else:
                pass  # suppress initial blank line
        else:
            self.saw_non_empty = True
            yield from self.lines  # yield blank lines from buffer
            self.lines.clear()
            yield line
