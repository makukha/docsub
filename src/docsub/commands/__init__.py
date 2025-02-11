from dataclasses import dataclass, field

from ..__base__ import Command, Config
from .exec import ExecCommand, ExecConfig
from .help import HelpCommand, HelpConfig
from .include import IncludeCommand, IncludeConfig
from .lines import LinesCommand
from .strip import StripCommand
from .x import XCommand, XConfig


COMMANDS: dict[str, type[Command]] = dict(
    exec=ExecCommand,
    help=HelpCommand,
    include=IncludeCommand,
    lines=LinesCommand,
    strip=StripCommand,
    x=XCommand,
)


@dataclass
class CmdConfig(Config):
    exec: ExecConfig = field(default_factory=ExecConfig)
    help: HelpConfig = field(default_factory=HelpConfig)
    include: IncludeConfig = field(default_factory=IncludeConfig)
    x: XConfig = field(default_factory=XConfig)
