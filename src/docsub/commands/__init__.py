from dataclasses import dataclass, field

from .base import BaseCommand, InvalidCommand
from .cat import CatCommand
from .help import HelpCommand


@dataclass
class CommandsConfig:
    cat: CatCommand.confclass = field(default_factory=CatCommand.confclass)
    help: HelpCommand.confclass = field(default_factory=HelpCommand.confclass)


COMMANDS: dict[str, BaseCommand] = {
    CatCommand.name: CatCommand,
    HelpCommand.name: HelpCommand,
}

def parse_command(statement: str, conf: CommandsConfig) -> BaseCommand:
    # get name
    try:
        name, args = statement.split(maxsplit=1)
    except Exception as exc:
        raise InvalidCommand(f'Invalid docsub command "{statement}"') from exc

    # validate name
    if name not in COMMANDS:
        raise InvalidCommand(f'Unknown docsub command name "{name}"')

    # instantiate command
    command = COMMANDS[name].from_args(args, conf=getattr(conf, name))
    return command
