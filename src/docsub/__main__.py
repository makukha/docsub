from pathlib import Path
from typing import Annotated

from cyclopts import App, Parameter
from cyclopts.types import ExistingFile

from . import __version__
from .config import load_config
from .process import process_paths


app = App(version=__version__)


@app.default
def docsub(
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


if __name__ == '__main__':
    app()
