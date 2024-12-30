from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
import re
import shlex
from subprocess import check_output
from typing import Self, override

from .base import BaseCommand, BaseConfig
from ..errors import RuntimeCommandError


@dataclass
class ShConfig(BaseConfig):
    env: dict[str, str] = field(default_factory=dict)


RX_CMDLINE = re.compile(r'(?P<cmdline>.+)')


@dataclass
class ShCommand(BaseCommand, name='sh', confclass=ShConfig):
    cmdline: str
    workdir: Path
    env: dict[str, str]

    @override
    @classmethod
    def from_args(cls, args: str, conf: ShConfig | None = None) -> Self | None:
        if (m := RX_CMDLINE.fullmatch(args)) is None:
            raise cls.invalid_args_error(args)
        conf = conf or ShConfig()
        return cls(
            cmdline=m.group('cmdline'),
            workdir=conf.workdir,
            env=conf.env,
        )

    @override
    def generate_lines(self) -> Iterable[str]:
        cmd = f"sh -c {shlex.quote(self.cmdline)}"
        try:
            result = check_output(
                shlex.split(cmd), env=self.env, text=True, cwd=self.workdir,
            )
        except Exception as exc:
            raise RuntimeCommandError(
                f'Command execution error: {self.cmdline}',
            ) from exc
        yield from result.splitlines()
