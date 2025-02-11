from collections.abc import Iterable
from contextlib import redirect_stdout
from dataclasses import dataclass
import io
from pathlib import Path
import re
import shlex
from typing import Optional

from typing_extensions import Unpack, override

from ..__base__ import (
    CmdKw,
    Config,
    DocsubfileError,
    Line,
    Location,
    Producer,
    Substitution,
)


DEFAULT_DOCSUBFILE_PATH = Path('docsubfile.py')


RX_CMD = re.compile(r'^\s*(?P<cmd>\S+)(\s+(?P<params>.*))?$')


@dataclass
class XConfig(Config):
    docsubfile: Path = DEFAULT_DOCSUBFILE_PATH


class XCommand(Producer, name='x'):
    conf: XConfig

    def __init__(self, args: str, *, conf: XConfig, **kw: Unpack[CmdKw]) -> None:
        super().__init__(args, conf=conf, **kw)
        if (match := RX_CMD.match(args)) is None:
            raise self.exc_invalid_args()
        name = match.group('cmd')
        cmd = self.env.x_group.commands.get(name, None)
        if cmd is None:
            raise DocsubfileError(
                f'Command "{name}" not found in "{conf.docsubfile}"', loc=self.loc
            )
        params = shlex.split(match.group('params'))
        self.cmd = cmd
        self.ctx = self.cmd.make_context(name, args=params, parent=self.env.ctx)

    @override
    def produce(self, sub: Optional[Substitution]) -> Iterable[Line]:
        out = io.StringIO()
        with redirect_stdout(out):
            self.cmd.invoke(self.ctx)
        for i, text in enumerate(out.getvalue().splitlines()):
            line = Line(text=text, loc=Location('stdout', lineno=i))
            yield line
