from pathlib import Path
from typing import Annotated

from loguru import logger
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from .commands import CommandsConfig
from .logging import LoggingConfig, configure_logging


DEFAULT_CONFIG_FILE = 'docsub.toml'
DEFAULT_DOCSUB_DIR = '.docsub'


class DocsubSettings(BaseSettings):
    local_dir: Path = Path(DEFAULT_DOCSUB_DIR)

    command: Annotated[CommandsConfig, Field(default_factory=CommandsConfig)]
    logging: Annotated[LoggingConfig, Field(default_factory=LoggingConfig)]

    model_config = SettingsConfigDict(
        cli_parse_args=True,
        env_prefix='DOCSUB_',
        nested_model_default_partial_update=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            TomlConfigSettingsSource(settings_cls),
        )


def load_config(config_file: Path, **kwargs) -> DocsubSettings:
    """Load config from file.
    """
    conf = DocsubSettings(_toml_file=config_file, **kwargs)
    configure_logging(conf.logging)
    logger.debug(f'Loaded configuration: {conf.model_dump_json()}')
    return conf
