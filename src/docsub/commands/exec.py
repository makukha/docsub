from collections.abc import Iterable
from dataclasses import dataclass, field
import os
import re
from subprocess import check_output
from typing import Self, override

from ..__base__ import Config, Line, Location, Producer, Substitution


@dataclass
class ExecConfig(Config):
    workdir: str = '.'
    env: dict[str, str] = field(default_factory=dict)


RX_CMD = re.compile(r'^\s*(?P<cmd>\S.*)$')


class ExecCommand(Producer, name='exec', conftype=ExecConfig):
    def __init__(self, cmd: str, *, conf: ExecConfig, loc: Location) -> None:
        super().__init__(loc)
        self.conf = conf
        self.cmd = cmd.strip()

    @override
    @classmethod
    def parse_args(cls, args: str, *, conf: Config | None, loc: Location) -> Self:
        conf = cls.assert_conf(conf, ExecConfig)
        if (match := RX_CMD.match(args)) is None:
            raise cls.error_invalid_args(args, loc=loc)
        return cls(cmd=match.group('cmd'), conf=conf, loc=loc)

    @override
    def produce(self, ctx: Substitution) -> Iterable[Line]:
        try:
            result = check_output(
                args=f'sh -c {self.cmd}',
                env=dict(os.environ) | self.conf.env,
                text=True,
                cwd=self.conf.workdir,
            )
        except Exception as exc:
            raise self.error_runtime(self.cmd) from exc

        for i, text in enumerate(result.splitlines()):
            line = Line(text=text, loc=Location('stdout', lineno=i))
            yield line
