from collections.abc import Iterable
from pathlib import Path

from ..config import Config

from .md import process_md_document


def process_paths(
    paths: Iterable[Path],
    *,
    in_place: bool = False,
    conf: Config,
) -> None:
    for path in paths:
        lines = process_md_document(path, conf=conf)
        if in_place:
            path.write_text(''.join(lines))
        else:
            for line in lines:
                print(line, end='')
