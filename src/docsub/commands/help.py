from collections.abc import Iterable
import os
import re
import shlex
import sys
from subprocess import check_output
from typing import Annotated, Unpack, override

from pydantic import Field

from ..__base__ import CmdKw, Config, Line, Location, Producer, Substitution


class HelpConfig(Config):
    env_vars: Annotated[dict[str, str], Field(default_factory=dict)]


CMD = r'[-._a-zA-Z0-9]+'
RX_CMD = re.compile(rf'^\s*(?P<python>python\s+-m\s+)?(?P<cmd>{CMD}(\s+{CMD})*)\s*$')


class HelpCommand(Producer, name='help'):
    conf: HelpConfig

    def __init__(self, args: str, *, conf: HelpConfig, **kw: Unpack[CmdKw]) -> None:
        super().__init__(args, conf=conf, **kw)
        if (match := RX_CMD.match(args)) is None:
            raise self.exc_invalid_args()
        self.use_python = bool(match.group('python'))
        self.cmd: str = match.group('cmd')

    @override
    def produce(self, sub: Substitution) -> Iterable[Line]:
        cmd = (
            f'{self.cmd} --help'
            if not self.use_python
            else f'{sys.executable} -m {self.cmd} --help'
        )
        try:
            result = check_output(
                args=shlex.split(cmd),
                env=dict(os.environ) | self.conf.env_vars,
                text=True,
            )
        except Exception as exc:
            raise self.exc_runtime_error(cmd) from exc

        for i, text in enumerate(result.splitlines()):
            line = Line(text=text, loc=Location('stdout', lineno=i))
            yield line
