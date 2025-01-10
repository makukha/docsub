from collections.abc import Iterable
from pathlib import Path
import re
from typing import Annotated, Self, override

from pydantic import Field

from ..__base__ import Config, Line, Location, Producer, Substitution


class IncludeConfig(Config):
    basedir: Annotated[Path, Field(default_factory=Path)]


RX_PATH = re.compile(r'^\s*(?P<path>\S.*)$')


class IncludeCommand(Producer, name='include', conftype=IncludeConfig):
    def __init__(self, path: str, conf: IncludeConfig, loc: Location) -> None:
        super().__init__(loc)
        self.conf = conf
        p = Path(path.strip())
        self.path = p if p.is_absolute() else (Path(self.conf.basedir) / p).resolve()

    @override
    @classmethod
    def parse_args(cls, args: str, *, conf: Config | None, loc: Location) -> Self:
        conf = cls.assert_conf(conf, IncludeConfig)
        if (match := RX_PATH.match(args)) is None:
            raise cls.error_invalid_args(args, loc=loc)
        return cls(path=match.group('path'), conf=conf, loc=loc)

    @override
    def produce(self, ctx: Substitution) -> Iterable[Line]:
        try:
            f = self.path.open('rt')
        except Exception as exc:
            raise self.error_runtime(f'Error opening file {self.path}') from exc
        with f:
            try:
                lineno = 0
                while text := f.readline():
                    line = Line(text=text, loc=Location(self.path, lineno=lineno))
                    yield line
                    lineno += 1
            except Exception as exc:
                raise self.error_runtime(f'Error reading file {self.path}') from exc
