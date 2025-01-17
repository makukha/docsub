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


TOML_FILE = 'docsub.toml'


class DocsubSettings(BaseSettings):
    tmp_dir: Path = Path('.docsub/tmp')
    commands_file: Path = Path('docsubfile.py')

    command: Annotated[CommandsConfig, Field(default_factory=CommandsConfig)]
    logging: Annotated[LoggingConfig, Field(default_factory=LoggingConfig)]

    model_config = SettingsConfigDict(
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


def load_config(toml_file: Path, **kwargs) -> DocsubSettings:
    """Load config from file.
    """
    conf = DocsubSettings(_toml_file=toml_file, **kwargs)
    configure_logging(conf.logging)
    logger.debug(f'Loaded configuration: {conf.model_dump_json()}')
    return conf
