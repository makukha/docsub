import importlib
import json
from pathlib import Path
import shlex
from typing import Annotated

import rich_click as click

from . import __version__
from .__base__ import Location
# from .commands import XCommand
from .environment import Environment
from .process import process_paths


@click.group()
@click.version_option(__version__, prog_name='docsub')
@click.option('-c', '--config-file', type=Path)
@click.option('-l', '--local-dir', type=Path)
@click.option( '--exec-work-dir', type=Path)
@click.option( '--exec-env-vars', type=str)
@click.option( '--help-env-vars', type=str)
@click.option( '--include-base-dir', type=Path)
@click.option( '-x', '--x-docsubfile', type=Path)
@click.pass_context
def app(
    ctx: click.Context,
    config_file: Path | None = None,
    # root settings
    local_dir: Path | None = None,
    # commands settings
    exec_work_dir: Path | None = None,
    exec_env_vars: str | None = None,
    help_env_vars: str | None = None,
    include_base_dir: Path | None = None,
    x_docsubfile: Path | None = None,

):
    def maybe_json_loads(value: str | None) -> dict | None:
        if value is not None:
            return json.loads(value)

    ctx.obj = Environment.from_config_file(
        config_file=config_file,
        options={
            'local_dir': local_dir,
            'cmd.exec.work_dir': exec_work_dir,
            'cmd.exec.env_vars': maybe_json_loads(exec_env_vars),
            'cmd.help.env_vars': maybe_json_loads(help_env_vars),
            'cmd.include.base_dir': include_base_dir,
            'cmd.x.docsubfile': x_docsubfile,
        },
    )


@app.command()
@click.argument('files', type=Path, nargs=-1, required=True)
@click.option('-i', '--in-place', is_flag=True, help='Process files in-place')
@click.pass_context
def apply(
    ctx: click.Context,
    files: tuple[Path, ...],
    in_place: bool = False,
):
    """
    Update Markdown files with embedded content.

    Read FILES and perform substitutions one by one. If one file depends on another,
    place it after that file.
    """
    process_paths(files, in_place=in_place, env=ctx.obj)


if __name__ == '__main__':
    app()
