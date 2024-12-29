from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass
class Location:
    filename: str | Path
    lineno: int | None = None

    def leader(self) -> str:
        if self.lineno:
            return f'"{self.filename}", line {self.lineno}: '
        else:
            return f'"{self.filename}": '


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
