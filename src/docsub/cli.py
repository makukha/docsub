from pathlib import Path

import rich_click as click

from . import __version__
from .process import process_paths


@click.command()
@click.option(
    '-i/ ', '--in-place/ ', is_flag=True, default=False, show_default=True,
    help='Overwrite source files.',
)
@click.version_option(__version__)
@click.argument(
    'file', nargs=-1,
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
)
def cli(file: list[str], in_place: bool):
    """
    Update documentation files with external content.
    """
    process_paths((Path(p) for p in file), in_place=in_place)
