from dataclasses import dataclass, field, fields
from pathlib import Path
import tomllib

from .commands import CommandsConfig, command


@dataclass
class DocsubConfig:
    command: CommandsConfig = field(default_factory=CommandsConfig)


def load_config(path: Path = Path('.docsub.toml')) -> DocsubConfig:
    """
    Load config from file.
    """
    if not path.exists():
        return DocsubConfig()
    conf = load_toml_config(path)
    return conf


def load_toml_config(path: Path) -> DocsubConfig:
    """
    Load  config from TOML file.
    """
    # get commands dict
    confdict = tomllib.loads(path.read_text())
    try:
        confdict = confdict['tool']['docsub']
    except KeyError as exc:
        raise ValueError('Invalid .docsub.toml config file') from exc
    cmd_dict: dict[str, dict] = confdict.get('command', {})

    # parse commands config
    cmd_values = {
        f.name: command[f.name].conftype(**cmd_dict.get(f.name, {}))  # type: ignore
        for f in fields(CommandsConfig)
        if command[f.name].conftype is not None
    }
    cmd_conf = CommandsConfig(**cmd_values)  # type: ignore
    return DocsubConfig(command=cmd_conf)
