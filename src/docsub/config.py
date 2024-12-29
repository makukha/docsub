from dataclasses import dataclass, field, fields
from pathlib import Path
import tomllib

from .commands import CommandsConfig


@dataclass
class Config:
    command: CommandsConfig = field(default_factory=CommandsConfig)


def load_config(path: Path = Path('.docsub.toml')) -> Config:
    if not path.exists():
        return Config()
    conf = parse_config(tomllib.loads(path.read_text()))
    return conf


def parse_config(confdict: dict) -> Config:
    commdict = confdict.get('command', {})
    commands = {
        cmd.name: cmd.type(**commdict.get(cmd.name, {}))
        for cmd in fields(CommandsConfig)
    }
    conf = Config(command=CommandsConfig(**commands))
    return conf
