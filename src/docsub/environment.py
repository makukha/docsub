from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

from click import Group
from pydantic import BaseModel

from .config import DEFAULT_CONFIG_FILE, DocsubSettings, load_config


@dataclass
class Environment:
    conf: DocsubSettings

    config_file: Path
    project_root: Path
    x: Group | None = None

    @classmethod
    def from_config_file(
        cls,
        config_file: Path | None,
        options: dict[str, Any] | None = None,
    ) -> Self:
        if config_file and Path(DEFAULT_CONFIG_FILE).exists():
            config_file = DEFAULT_CONFIG_FILE
        conf = load_config(config_file)
        env = cls(
            conf=conf,
            config_file=config_file,
            project_root=(config_file.parent if config_file else Path('.')).resolve(),
        )
        env._update_options(options)
        return env

    @property
    def local_dir(self) -> Path:
        return self._from_project_root(self.conf.local_dir)

    def provide_temp_dir(self, name: str | Path) -> Path:
        path = self.local_dir / f'tmp_{name}'
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _from_project_root(self, path: Path) -> Path:
        return (path if path.is_absolute() else self.project_root / path).resolve()

    def _update_options(self, options: dict[str, Any] | None) -> None:
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
                        f'Nested attributes not allowed for {'.'.join(attrs[:i])}'
                    )
                if i == len(attrs) - 1:  # last attribute
                    setattr(item, a, options[opt])
                else:
                    item = getattr(item, a)
