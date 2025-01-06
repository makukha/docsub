from collections.abc import Iterable
from dataclasses import dataclass, field
import os
import re
import shlex
import sys
from subprocess import check_output
from typing import Self, override

from ..__base__ import Config, Line, Location, Producer, Substitution


@dataclass
class HelpConfig(Config):
    env: dict[str, str] = field(default_factory=dict)


CMD = r'[-._a-zA-Z0-9]+'
RX_CMD = re.compile(fr'^\s*(?P<python>python\s+-m\s+)?(?P<cmd>{CMD}(\s+{CMD})*)\s*$')


class HelpCommand(Producer, name='help', conftype=HelpConfig):
    def __init__(self, cmd: str, use_python: bool, conf: HelpConfig, loc: Location) -> None:
        super().__init__(loc)
        self.conf = conf
        self.cmd = cmd.strip()
        self.use_python = use_python

    @override
    @classmethod
    def parse_args(cls, args: str, *, conf: Config | None, loc: Location) -> Self:
        conf = cls.assert_conf(conf, HelpConfig)
        if (m := RX_CMD.match(args)) is None:
            raise cls.error_invalid_args(args, loc=loc)
        return cls(cmd=m.group('cmd'), use_python=bool(m.group('python')), conf=conf, loc=loc)

    @override
    def produce(self, ctx: Substitution) -> Iterable[Line]:
        cmd = (
            f'{self.cmd} --help'
            if not self.use_python
            else f'{sys.executable} -m {self.cmd} --help'
        )
        try:
            result = check_output(
                args=shlex.split(cmd),
                env=dict(os.environ) | self.conf.env,
                text=True,
            )
        except Exception as exc:
            raise self.error_runtime(cmd) from exc

        for i, text in enumerate(result.splitlines()):
            line = Line(text=text, loc=Location('stdout', lineno=i))
            yield line
