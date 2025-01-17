from collections.abc import Iterable
from pathlib import Path

from .environment import Environment
from .processors.md import MarkdownProcessor


def process_paths(
    paths: Iterable[Path],
    *,
    in_place: bool = False,
    env: Environment,
) -> None:
    proc_md = MarkdownProcessor(env.conf)
    for path in paths:
        lines = proc_md.process_document(path)  # iterator
        if in_place:
            path.write_text(''.join(lines))
        else:
            for line in lines:
                print(line, end='')
