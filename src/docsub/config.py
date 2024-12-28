from pathlib import Path
import tomllib


def load_config(path: Path = Path('.docsub.toml')) -> dict:
    if path.exists():
        return tomllib.loads(path.read_text())
    else:
        return {}
