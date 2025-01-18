from collections.abc import Iterable
from pathlib import Path
from typing import Annotated, override

from pydantic import Field

from ..__base__ import Config, Line, Location, Producer, Substitution


class IncludeConfig(Config):
    base_dir: Annotated[Path, Field(default_factory=Path)]


class IncludeCommand(Producer, name='include'):
    conf: IncludeConfig

    def __init__(self, args: str, *, conf: IncludeConfig, loc: Location, **kw) -> None:
        super().__init__(args, loc=loc, conf=conf)
        args = args.strip()
        if not args:
            raise self.exc_invalid_args()
        path = Path(args)
        if not path.is_absolute():
            path = self.conf.base_dir / path
        self.path = path.resolve()
        if not self.path.exists():
            raise self.exc_runtime_error(f'File "{self.path}" not found')

    @override
    def produce(self, sub: Substitution) -> Iterable[Line]:
        try:
            with self.path.open('rt') as f:
                lineno = 0
                while text := f.readline():
                    line = Line(text=text, loc=Location(self.path, lineno=lineno))
                    yield line
                    lineno += 1
        except Exception as exc:
            raise self.exc_runtime_error(f'Error reading file {self.path}') from exc
