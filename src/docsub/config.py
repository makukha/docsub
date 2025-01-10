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


class DocsubSettings(BaseSettings):
    command: Annotated[CommandsConfig, Field(default_factory=CommandsConfig)]
    logging: Annotated[LoggingConfig, Field(default_factory=LoggingConfig)]

    model_config = SettingsConfigDict(
        env_prefix='DOCSUB_',
        env_nested_delimiter='_',
        nested_model_default_partial_update=True,
        toml_file='.docsub.toml',
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


def load_config() -> DocsubSettings:
    """
    Load config from file.
    """
    conf = DocsubSettings()  # type: ignore
    configure_logging(conf.logging)  # type: ignore
    logger.debug(f'Loaded configuration: {conf.model_dump_json()}')
    return conf
