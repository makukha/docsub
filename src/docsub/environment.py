from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any, Optional, Union

from importloc import import_module_from_file
from pydantic import BaseModel
import rich_click as click
from typing_extensions import Self

from .__base__ import DocsubfileError, DocsubfileNotFound
from .config import DEFAULT_CONFIG_FILE, DocsubSettings, load_config


@dataclass
class Environment:
    conf: DocsubSettings
    ctx: click.Context

    config_file: Optional[Path]
    project_root: Path

    @classmethod
    def from_config_file(
        cls,
        ctx: click.Context,
        config_file: Optional[Path],
        options: Optional[dict[str, Any]] = None,
    ) -> Self:
        if not config_file and DEFAULT_CONFIG_FILE.exists():
            config_file = DEFAULT_CONFIG_FILE
        conf = load_config(config_file)
        env = cls(
            conf=conf,
            ctx=ctx,
            config_file=config_file,
            project_root=(config_file.parent if config_file else Path('.')).resolve(),
        )
        env._update_options(options)
        return env

    @property
    def local_dir(self) -> Path:
        return self._from_project_root(self.conf.local_dir)

    @cached_property
    def x_group(self) -> click.Group:
        path = self.conf.cmd.x.docsubfile
        if not path.exists():
            raise DocsubfileNotFound(f'Docsubfile "{path}" not found')
        docsubfile = import_module_from_file(path, 'docsubfile', replace=True)
        if not hasattr(docsubfile, 'x') or not isinstance(docsubfile.x, click.Group):
            raise DocsubfileError(f'Docsubfile "{path}" has no valid "x" group')
        return docsubfile.x

    def get_temp_dir(self, name: Union[str, Path]) -> Path:
        path = self.local_dir / f'tmp_{name}'
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _from_project_root(self, path: Path) -> Path:
        return (path if path.is_absolute() else self.project_root / path).resolve()

    def _update_options(self, options: Optional[dict[str, Any]]) -> None:
        if not options:
            return
        for opt in (k for k, v in options.items() if v is not None):
            item = self.conf
            attrs = opt.split('.')
            for i, a in enumerate(attrs):
                if not hasattr(item, a):
                    raise ValueError(f'Invalid option "{opt}"')
                if not isinstance(getattr(item, a), BaseModel) and i < len(attrs) - 1:
                    raise TypeError(
                        f'Nested attributes not allowed for {".".join(attrs[:i])}'
                    )
                if i == len(attrs) - 1:  # last attribute
                    setattr(item, a, options[opt])
                else:
                    item = getattr(item, a)


pass_env = click.make_pass_decorator(Environment)
