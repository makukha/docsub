from collections.abc import Iterable


def add_ending_newline(lines: Iterable[str]) -> Iterable[str]:
    for line in lines:
        yield line if line.endswith('\n') else f'{line}\n'
