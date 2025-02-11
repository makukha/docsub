from collections.abc import Iterable
from dataclasses import asdict, dataclass, field, is_dataclass
import json
import os
from pathlib import Path
from typing import Any, Optional, Union
import warnings

from loguru import logger
from typing_extensions import Self

try:
    import tomllib  # type: ignore[import-not-found,unused-ignore]
except ImportError:
    import tomli as tomllib  # type: ignore[import-not-found,unused-ignore]

from .__base__ import Config
from .commands import CmdConfig
from .logging import LoggingConfig


DEFAULT_CONFIG_FILE = Path('docsub.toml')
DEFAULT_CONFIG_ROOT = 'tool.docsub'
DEFAULT_DOCSUB_DIR = Path('.docsub')
DEFAULT_ENV_PREFIX = 'DOCSUB_'


@dataclass
class DocsubConfig(Config):
    local_dir: Path = DEFAULT_DOCSUB_DIR

    cmd: CmdConfig = field(default_factory=CmdConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    @classmethod
    def load(cls,
        config_file: Optional[Path] = None,
        configure_logging: bool = True,
    ) -> Self:
        conf = cls()
        if config_file is not None:
            conf.update_from_toml(config_file)
        conf.update_from_env()
        if configure_logging:
            conf.logging.configure()
        # finish
        text = json.dumps(asdict(conf), separators=(' ', ' '), cls=JSONEncoder)
        logger.debug(f'Loaded configuration {text}')
        return conf

    def update_from_dict(self, values: dict[str, Any]) -> None:
        update_from_dict(self, values)

    def update_from_env(self, env_prefix: str = DEFAULT_ENV_PREFIX) -> None:
        for name in os.environ:
            if not name.startswith(env_prefix):
                continue
            try:
                setattr_separated(self, name[len(env_prefix):], os.environ[name])
            except AttributeError:
                msg = 'Environment variable {} does not match any config option'.format(name)
                warnings.warn(msg, EnvironmentVariableWarning, stacklevel=2)
                pass

    def update_from_options(self, values: Optional[dict[str, Any]]) -> None:
        if not values:
            return
        for opt in (k for k, v in values.items() if v is not None):
            item = self
            attrs = opt.split('.')
            for i, a in enumerate(attrs):
                # validate
                if not is_dataclass(item):
                    raise ValueError(f'Nested attribute not allowed for {type(item)}')
                if not hasattr(item, a):
                    raise ValueError(f'Invalid option {opt}')
                # set or next
                if i == len(attrs) - 1:  # last attribute
                    setattr(item, a, values[opt])
                else:
                    item = getattr(item, a)

    def update_from_toml(self, path: Union[Path, str], root: str = DEFAULT_CONFIG_ROOT) -> None:
        with Path(path).open('rb') as fp:
            data = tomllib.load(fp)

        if root != '.':
            for attr in root.split('.'):
                data = data[attr]

        self.update_from_dict(data)


class EnvironmentVariableWarning(UserWarning): ...


def update_from_dict(item: Any, values: dict[str, Any]) -> None:
    if not is_dataclass(item):
        raise ValueError(f'Nested attribute not allowed for {type(item)}')

    for k, v in values.items():
        if not hasattr(item, k):
            msg = 'Dataclass {} has no attribute {}'.format(type(item), k)
            raise AttributeError(msg)
        elif not is_dataclass(getattr(item, k)):
            setattr(item, k, v)
        else:
            update_from_dict(getattr(item, k), v)


def setattr_separated(item: Any, name: str, value: Any, sep: str='_') -> None:
    if not is_dataclass(item):
        raise ValueError(f'Nested attribute not allowed for {type(item)}')

    if hasattr(item, name):
        setattr(item, name, value)  # short circuit

    for attr in separated_prefixes(name, sep):
        if hasattr(item, attr):
            setattr_separated(
                item=getattr(item, attr),
                name=name[len(attr) + len(sep) :],
                value=value,
                sep=sep,
            )
        return

    msg = 'Dataclass {} attribute chain {} not matched'.format(type(item), name)
    raise AttributeError(msg)


def separated_prefixes(name: str, sep: str) -> Iterable[str]:
    end = -1
    while True:
        end = name.index(sep, end + 1)
        if end == -1:
            yield name
            break
        else:
            yield name[:end]


class JSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Path):
            return str(o)
        return super().default(o)
