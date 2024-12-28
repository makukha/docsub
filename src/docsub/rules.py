from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path
import re
import shlex
from subprocess import check_output
import sys
from typing import Self

from .config import load_config

conf = load_config()


class Rule(ABC):
    @classmethod
    @abstractmethod
    def match(cls, command: str) -> Self | None:
        raise NotImplementedError

    @abstractmethod
    def lines(self) -> Iterable[str]:
        raise NotImplementedError


class InvalidRule(ValueError):
    def __init__(self, value: str) -> None:
        super().__init__(f'Invalid docsub rule: {value}')


class CatRule(Rule):
    def __init__(self, files: Iterable[Path | str]) -> None:
        self.files: tuple[Path, ...] = tuple(Path(f) for f in files)

    RX_COMMAND = re.compile(r'\s*cat\s+(?P<files>\S.+)')

    @classmethod
    def match(cls, command: str) -> Self | None:
        if (m := cls.RX_COMMAND.fullmatch(command)) is None:
            return None
        return cls(files=shlex.split(m.group('files')))

    def resolve(self, cwd: Path) -> None:
        self.files = tuple(
            (cwd / f).resolve() if not f.is_absolute() else f
            for f in self.files
        )

    def lines(self) -> Iterable[str]:
        for path in self.files:
            with path.open('rt') as f:
                while line := f.readline():
                    yield line


class HelpRule(Rule):
    def __init__(self, python: str | None, utility: str) -> None:
        self.conf = conf.get('command', {}).get('help', {})
        self.python = sys.executable if python else None
        self.utility = utility

    RX_COMMAND = re.compile(r'\s*help\s+(?P<python>python\s+-m\s+)?(?P<utility>\S+)')

    @classmethod
    def match(cls, command: str) -> Self | None:
        if (m := cls.RX_COMMAND.fullmatch(command)) is None:
            return None
        return cls(**m.groupdict())

    def lines(self) -> Iterable[str]:
        python = [self.python, '-m'] if self.python else []
        result = check_output(
            [*python, self.utility, '--help'],
            env=self.conf.get('env', {}),
            text=True,
        )
        yield from result.splitlines()
