from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Self

from ..errors import InvalidCommand


@dataclass
class BaseConfig:
    workdir: Path | str = field(default_factory=Path)

    def __post_init__(self):
        if not isinstance(self.workdir, Path):
            self.workdir = Path(self.workdir)


class BaseCommand[C: BaseConfig](ABC):
    name: ClassVar[str]
    confclass: ClassVar[type[BaseConfig]]

    def __init_subclass__(
        cls,
        *,
        name: str,
        confclass: type[BaseConfig],
        **kwargs,
    ) -> type[Self]:
        cls.name = name
        cls.confclass = confclass
        super().__init_subclass__(**kwargs)

    @classmethod
    @abstractmethod
    def from_args(cls, args: str, conf: C | None = None) -> Self:
        raise NotImplementedError

    @abstractmethod
    def generate_lines(self) -> Iterable[str]:
        raise NotImplementedError

    @classmethod
    def invalid_args_error(cls, args: str) -> 'InvalidCommand':
        return InvalidCommand(f'Invalid docsub "{cls.name}" args: {args}')
