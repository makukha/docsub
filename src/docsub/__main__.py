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
    in_place: Annotated[bool, Parameter(name=('--in-place', '-i'))] = False,
    *file: ExistingFile,
):
    """
    Update Markdown files with embedded content.

    Parameters
    ----------
    in_place
        Process files in-place.
    file
        Markdown files to be processed in order.
    """
    process_paths((Path(p) for p in file), in_place=in_place, conf=load_config())


if __name__ == '__main__':
    app()
