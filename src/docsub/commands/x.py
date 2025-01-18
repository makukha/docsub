from collections.abc import Iterable
from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import shlex
from typing import TYPE_CHECKING, override

from ..__base__ import Config, DocsubfileError, Line, Location, Producer, Substitution
if TYPE_CHECKING:
    from ..environment import Environment  # noqa: F401


RX_CMD = re.compile(r'^\s*(?P<cmd>\S+)(\s+(?P<params>.*))?$')


class XConfig(Config):
    docsubfile: Path = Path('docsubfile.py')


class XCommand(Producer, name='x'):
    conf: XConfig

    def __init__(
        self,
        args: str,
        *,
        conf: XConfig,
        loc: Location,
        env,  # type: Environment
    ) -> None:
        super().__init__(args, loc=loc, conf=conf, env=env)
        self.ctx = env.ctx
        if (match := RX_CMD.match(args)) is None:
            raise self.exc_invalid_args()
        name = match.group('cmd')
        cmd = env.x_group.commands.get(name, None)
        if cmd is None:
            raise DocsubfileError(
                f'Command "{name}" not found in "{conf.docsubfile}"', loc=loc
            )
        params = shlex.split(match.group('params'))
        self.cmd = cmd
        self.ctx = self.cmd.make_context(name, args=params, parent=env.ctx)

    @override
    def produce(self, sub: Substitution | None) -> Iterable[Line]:
        out = io.StringIO()
        with redirect_stdout(out):
            self.cmd.invoke(self.ctx)
        for i, text in enumerate(out.getvalue().splitlines()):
            line = Line(text=text, loc=Location('stdout', lineno=i))
            yield line
