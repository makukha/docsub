from pathlib import Path
import shlex
from typing import Annotated

from cyclopts import App, Parameter
from cyclopts.types import ExistingFile

from . import __version__
from .__base__ import Location
from .commands import XCommand
from .config import load_config
from .process import process_paths


app = App(name='docsub', version=__version__)


@app.command
def apply(
    file: Annotated[list[ExistingFile], Parameter(negative=())],
    /,
    in_place: Annotated[bool, Parameter(('--in-place', '-i'), negative=())] = False,
):
    """
    Update Markdown files with embedded content.

    Parameters
    ----------
    file
        Markdown files to be processed in order.
    in_place
        Process files in-place.
    """
    process_paths((Path(p) for p in file), in_place=in_place, conf=load_config())


@app.command
def x(
    command: Annotated[str, Parameter(negative=())],
    /,
    *params,
):
    """
    Execute user-defined custom command from local docsubfile.py.

    Parameters
    ----------
    command
        Custom command name.
    params
        Custom command parameters.
    """
    producer = XCommand(
        cmd=command,
        params=shlex.join(params),
        loc=Location('<command line>'),
    )
    for line in producer.produce(None):
        print(line.text, end='')


if __name__ == '__main__':
    app()
