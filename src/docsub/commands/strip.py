from typing import Iterable, override

from ..__base__ import Substitution, Line, Location, Modifier


class StripCommand(Modifier, name='strip'):
    def __init__(self, args: str, *, loc: Location, **kw) -> None:
        super().__init__(args, loc=loc)
        if args.strip():
            raise self.exc_invalid_args()
        self.lines: list[Line] = []
        self.saw_non_empty = False

    @override
    def on_produced_line(self, line: Line, sub: Substitution) -> Iterable[Line]:
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
