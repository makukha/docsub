from collections.abc import Iterable
from pathlib import Path
import re
import shlex
from subprocess import check_output
import sys
from typing import Any, Self, override

from ..__base__ import DocsubError, Line, Location, Producer, Substitution


DOCSUBFILE = Path('docsubfile.py').resolve()
RX_CMD = re.compile(r'^\s*(?P<cmd>\S+)(\s+(?P<opts>.*))?$')


class DocsubfileNotFound(DocsubError, FileNotFoundError): ...


class XCommand(Producer, name='x'):
    def __init__(self, cmd: str, opts: str | None, *, loc: Location) -> None:
        super().__init__(loc)
        self.cmd = cmd
        self.opts = opts.strip() if opts else None

    @override
    @classmethod
    def parse_args(cls, args: str, *, conf: Any = None, loc: Location) -> Self:
        if not DOCSUBFILE.exists():
            raise DocsubfileNotFound(
                f'Docsubfile file not found: {DOCSUBFILE}', loc=loc
            )
        if (match := RX_CMD.match(args)) is None:
            raise cls.error_invalid_args(args, loc=loc)
        return cls(cmd=match.group('cmd'), opts=match.group('opts'), loc=loc)

    @override
    def produce(self, ctx: Substitution) -> Iterable[Line]:
        python = sys.executable
        cmd = [python, str(DOCSUBFILE), self.cmd]
        if self.opts:
            cmd.extend(shlex.split(self.opts))
        try:
            result = check_output(args=cmd, text=True)
        except Exception as exc:
            raise self.error_runtime(self.cmd) from exc

        for i, text in enumerate(result.splitlines()):
            line = Line(text=text, loc=Location('stdout', lineno=i))
            yield line
