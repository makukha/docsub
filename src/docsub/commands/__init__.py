from typing import Annotated

from pydantic import Field

from ..__base__ import Command, Config
from .exec import ExecCommand, ExecConfig
from .help import HelpCommand, HelpConfig
from .include import IncludeCommand, IncludeConfig
from .lines import LinesCommand
from .strip import StripCommand
from .x import XCommand


COMMANDS: dict[str, type[Command]] = dict(
    exec=ExecCommand,
    help=HelpCommand,
    include=IncludeCommand,
    lines=LinesCommand,
    strip=StripCommand,
    x=XCommand,
)


class CommandsConfig(Config):
    exec: Annotated[ExecConfig, Field(default_factory=ExecConfig)]
    help: Annotated[HelpConfig, Field(default_factory=HelpConfig)]
    include: Annotated[IncludeConfig, Field(default_factory=IncludeConfig)]
