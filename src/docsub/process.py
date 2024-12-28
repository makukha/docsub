from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Self, assert_never

from .rules import CatRule, HelpRule, Rule


def process_paths(
    paths: Iterable[Path],
    *,
    in_place: bool = False,
    cwd: Path | None = None,
) -> None:
    for path in paths:
        lines = process_md_document(path, cwd=cwd or Path('.'))
        if in_place:
            path.write_text(''.join(lines))
        else:
            for line in lines:
                print(line, end='')


RX_MD_FENCE = re.compile(
    r'(?P<space>\s*)(?P<fence>```+)\s*(?P<syntax>((?!<-)\S)+)?'
    '(?:\s*<-\s*(?P<command>.*)|.*)',
    flags=re.DOTALL,
)


@dataclass
class MdFence:
    space: str
    fence: str
    syntax: str = field(compare=False)
    command: str = field(compare=False)

    @classmethod
    def from_line(cls, line: str) -> Self | None:
        if match := RX_MD_FENCE.fullmatch(line.rstrip()):  # remove trailing newline
            return cls(**match.groupdict())


def match_rule(command: str | None) -> Rule | None:
    if command:
        for rule_class in (
            CatRule,
            HelpRule,
        ):
            if rule := rule_class.match(command):
                return rule


def process_md_document(file: Path, *, cwd: Path) -> Iterable[str]:
    fences = []
    rules = []

    with file.open('rt') as f:
        while line := f.readline():

            # not a fenced block delimiter line
            if not (fence := MdFence.from_line(line)):
                if not any(rules):
                    yield line

            # current fenced block delimiter line
            elif len(fences) and fence == fences[-1]:
                if not any(rules) or rules[-1]:
                    yield line
                fences.pop()
                rules.pop()

            # new fenced block delimiter line
            else:
                if not any(rules):
                    yield line
                fences.append(fence)
                rules.append(None if any(rules) else match_rule(fence.command))

                match rules[-1]:
                    case CatRule():
                        rules[-1].resolve(cwd)  # type: CatRule
                        yield from ensure_ending_newline(rules[-1].lines())

                    case HelpRule():
                        yield from ensure_ending_newline(rules[-1].lines())

                    case None:
                        pass

                    case _:
                        assert_never(rules[-1])


def ensure_ending_newline(lines: Iterable[str]) -> Iterable[str]:
    for line in lines:
        yield line if line.endswith('\n') else f'{line}\n'
