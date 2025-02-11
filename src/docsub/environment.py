from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any, Optional, Union

from importloc import Location
import rich_click as click
from typing_extensions import Self

from .__base__ import DocsubfileError, DocsubfileNotFound
from .config import DocsubConfig


@dataclass
class Environment:
    conf: DocsubConfig
    ctx: click.Context

    config_file: Optional[Path]
    project_root: Path

    @classmethod
    def from_config_file(
        cls,
        ctx: click.Context,
        config_file: Optional[Path] = None,
        options: Optional[dict[str, Any]] = None,
    ) -> Self:
        conf = DocsubConfig.load(config_file=config_file, configure_logging=True)
        conf.update_from_options(options)
        env = cls(
            conf=conf,
            ctx=ctx,
            config_file=config_file,
            project_root=(config_file.parent if config_file else Path('.')).resolve(),
        )
        return env

    @property
    def local_dir(self) -> Path:
        return self._from_project_root(self.conf.local_dir)

    @cached_property
    def x_group(self) -> click.Group:
        path = self.conf.cmd.x.docsubfile
        if not path.exists():
            raise DocsubfileNotFound(f'Docsubfile "{path}" not found')
        docsubfile = Location(path).load('docsubfile', on_conflict='replace')
        if not hasattr(docsubfile, 'x') or not isinstance(docsubfile.x, click.Group):
            raise DocsubfileError(f'Docsubfile "{path}" has no valid "x" group')
        return docsubfile.x

    def get_temp_dir(self, name: Union[str, Path]) -> Path:
        path = self.local_dir / f'tmp_{name}'
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _from_project_root(self, path: Path) -> Path:
        return (path if path.is_absolute() else self.project_root / path).resolve()


pass_env = click.make_pass_decorator(Environment)
