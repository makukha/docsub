from collections.abc import Iterable
import os
from pathlib import Path
from subprocess import check_output
from typing import Annotated, override

from pydantic import Field

from ..__base__ import Config, Line, Location, Producer, Substitution


class ExecConfig(Config):
    work_dir: Annotated[Path, Field(default_factory=Path)]
    env_vars: Annotated[dict[str, str], Field(default_factory=dict)]


class ExecCommand(Producer, name='exec'):
    conf: ExecConfig

    def __init__(self, args: str, *, loc: Location, conf: ExecConfig, **kw) -> None:
        super().__init__(args, loc=loc, conf=conf, env=None)
        commands = args.strip()
        if not commands:
            raise self.exc_invalid_args()
        self.commands = commands

    @override
    def produce(self, sub: Substitution) -> Iterable[Line]:
        try:
            result = check_output(
                args=['sh', '-c', self.commands],
                env=dict(os.environ) | self.conf.env_vars,
                text=True,
                cwd=self.conf.work_dir,
            )
        except Exception as exc:
            raise self.exc_runtime_error(self.commands) from exc

        for i, text in enumerate(result.splitlines()):
            line = Line(text=text, loc=Location('stdout', lineno=i))
            yield line
