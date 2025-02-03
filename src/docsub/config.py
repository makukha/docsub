from pathlib import Path
from typing import Annotated, Any

from loguru import logger
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from .commands import CmdConfig
from .logging import LoggingConfig, configure_logging


DEFAULT_CONFIG_FILE = Path('docsub.toml')
DEFAULT_DOCSUB_DIR = Path('.docsub')


class DocsubSettings(BaseSettings):
    local_dir: Path = DEFAULT_DOCSUB_DIR

    cmd: Annotated[CmdConfig, Field(default_factory=CmdConfig)]
    logging: Annotated[LoggingConfig, Field(default_factory=LoggingConfig)]

    model_config = SettingsConfigDict(
        env_prefix='DOCSUB_',
        nested_model_default_partial_update=True,
        toml_file=[],
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


def load_config(config_file: Path | None, **kwargs: dict[str, Any]) -> DocsubSettings:
    """Load config from file."""
    if config_file:
        DocsubSettings.model_config['toml_file'] = [config_file]
    conf = DocsubSettings(**kwargs)  # type: ignore
    configure_logging(conf.logging)
    logger.debug(f'Loaded configuration: {conf.model_dump_json()}')
    return conf
