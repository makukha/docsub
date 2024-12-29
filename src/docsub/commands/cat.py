from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
import shlex
from typing import Self, override

from .base import BaseCommand, BaseConfig
from ..errors import RuntimeCommandError


@dataclass
class CatConfig(BaseConfig):
    ...


@dataclass
class CatCommand(BaseCommand, name='cat', confclass=CatConfig):
    files: tuple[Path, ...] | Iterable[Path | str]

    def __post_init__(self):
        self.files = tuple(Path(f) for f in self.files)

    @override
    @classmethod
    def from_args(cls, args: str, conf: CatConfig | None = None) -> Self:
        try:
            paths = shlex.split(args)
        except Exception as exc:
            raise cls.invalid_args_error(args) from exc
        conf = conf or CatConfig()
        files = tuple(
            path if path.is_absolute() else (conf.workdir / path).resolve()
            for path in (Path(p) for p in paths)
        )
        return cls(files)


    @override
    def generate_lines(self) -> Iterable[str]:
        for path in self.files:
            try:
                with path.open('rt') as f:
                    while line := f.readline():
                        yield line
            except Exception as exc:
                raise RuntimeCommandError(f'File error: {path}') from exc
