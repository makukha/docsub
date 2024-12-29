from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
import re
import shlex
from subprocess import check_output
import sys
from typing import Self, override

from .base import BaseCommand, BaseConfig
from ..errors import RuntimeCommandError


@dataclass
class HelpConfig(BaseConfig):
    env: dict[str, str] = field(default_factory=dict)


RX_ARGS = re.compile(r'(?P<python>python\s+-m)?\s*(?P<util>\S+)')


@dataclass
class HelpCommand(BaseCommand, name='help', confclass=HelpConfig):
    python: bool
    util: str
    workdir: Path
    env: dict[str, str]

    @override
    @classmethod
    def from_args(cls, args: str, conf: HelpConfig | None = None) -> Self | None:
        if (m := RX_ARGS.fullmatch(args)) is None:
            raise cls.invalid_args_error(args)
        conf = conf or HelpConfig()
        return cls(
            python=bool(m.group('python')),
            util=m.group('util'),
            workdir=conf.workdir,
            env=conf.env,
        )

    @override
    def generate_lines(self) -> Iterable[str]:
        python = [sys.executable, '-m'] if self.python else []
        cmd = [*python, self.util, '--help']
        try:
            result = check_output(cmd, env=self.env, text=True, cwd=self.workdir)
        except Exception as exc:
            raise RuntimeCommandError(
                f'Command execution error: {shlex.join(cmd)}',
            ) from exc
        yield from result.splitlines()
