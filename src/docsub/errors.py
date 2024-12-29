from dataclasses import dataclass
from pathlib import Path


@dataclass
class Location:
    filename: str | Path
    lineno: int | None = None
    colno: int | None = None

    def leader(self) -> str:
        return ', '.join((
            f'"{self.filename}"',
            *((f'line {self.lineno}',) if self.lineno is not None else ()),
            *((f'col {self.colno}',) if self.colno is not None else ()),
        )) + ': '


@dataclass
class DocsubError(Exception):
    message: str
    loc: Location | None = None

    def __str__(self) -> str:
        if self.loc:
            return f'{self.loc.leader()}{self.message}'
        else:
            return self.message


class InvalidCommand(DocsubError):
    ...


class RuntimeCommandError(DocsubError):
    ...
