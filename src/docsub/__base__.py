from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from typing import Any, ClassVar, Self

from pydantic import BaseModel as Config


# syntax


@dataclass
class Location:
    """
    Location in file.
    """

    fname: str | Path
    lineno: int | None = None
    colno: int | None = None

    def leader(self) -> str:
        parts = (
            f'"{self.fname}"',
            *((f'line {self.lineno}',) if self.lineno is not None else ()),
            *((f'col {self.colno}',) if self.colno is not None else ()),
        )
        return f'{", ".join(parts)}: '


@dataclass
class SyntaxElement(ABC):
    """
    Base syntax element.
    """

    loc: Location


@dataclass
class Line(SyntaxElement):
    """
    Line in file.
    """

    text: str

    def __post_init__(self) -> None:
        if not self.text.endswith('\n'):
            self.text += '\n'


# substitution


@dataclass(kw_only=True)
class Substitution(SyntaxElement, ABC):
    """
    Base substitution request.
    """

    id: str | None = None
    conf: Any
    producers: list['Producer'] = field(default_factory=list)
    modifiers: list['Modifier'] = field(default_factory=list)

    @classmethod
    @abstractmethod
    def match(cls, line: Line, conf: Any) -> Self | None:
        raise NotImplementedError

    @abstractmethod
    def consume_line(self, line: Line) -> Iterable[Line]:
        raise NotImplementedError

    # helpers

    def append_command(self, cmd: 'Command') -> None:
        if isinstance(cmd, Producer):
            self.producers.append(cmd)
        elif isinstance(cmd, Modifier):
            self.modifiers.append(cmd)
        else:
            raise TypeError(f'Expected Command, received {type(cmd)}')

    @classmethod
    def error_invalid(cls, value: str, loc: Location) -> 'InvalidSubstitution':
        return InvalidSubstitution(f'Invalid docsub substitution: {value}', loc=loc)

    # processing

    def process_content_line(self, line: Line) -> None:
        for cmd in self.modifiers:
            cmd.on_content_line(line, self)

    def produce_lines(self) -> Iterable[Line]:
        for mod_cmd in self.modifiers:
            yield from mod_cmd.before_producers(self)
        for prod_cmd in self.producers:
            for line in prod_cmd.produce(self):
                yield from self._modified_lines(line)
        for mod_cmd in self.modifiers:
            yield from mod_cmd.after_producers(self)

    def _modified_lines(self, line: Line) -> Iterable[Line]:
        lines = (line,)  # type: tuple[Line, ...]
        for cmd in self.modifiers:
            lines = tuple(
                chain.from_iterable(cmd.on_produced_line(ln, self) for ln in lines)
            )
        yield from lines


class Command(ABC):
    """
    Base command.
    """

    name: ClassVar[str]
    conftype: ClassVar[type[Config] | None]

    loc: Location

    def __init__(self, loc: Location) -> None:
        self.loc = loc

    @classmethod
    @abstractmethod
    def parse_args(cls, args: str, *, conf: Config | None, loc: Location) -> Self:
        raise NotImplementedError

    # error helpers

    @classmethod
    def assert_conf[C: Config](cls, conf: Config | None, conf_class: type[C]) -> C:
        if not isinstance(conf, conf_class):
            raise TypeError(f'Expected {conf_class}, received {type(conf)}')
        return conf

    @classmethod
    def error_invalid_args(cls, args: str, loc: Location) -> 'InvalidCommand':
        return InvalidCommand(
            f'Invalid docsub command "{cls.name}" args: {args}',
            loc=loc,
        )

    def error_runtime(self, args: Any) -> 'RuntimeCommandError':
        return RuntimeCommandError(
            f'Runtime error in "{self.name}" command: {args}',
            loc=self.loc,
        )


class Producer(Command, ABC):
    """
    Base producing command.
    """

    def __init_subclass__(
        cls,
        *,
        name: str,
        conftype: type[Config] | None = None,
        **kwargs,
    ):
        super().__init_subclass__(**kwargs)
        cls.name = name
        cls.conftype = conftype

    @abstractmethod
    def produce(self, ctx: Substitution) -> Iterable[Line]:
        raise NotImplementedError


class Modifier(Command, ABC):
    """
    Base modifying command.
    """

    def __init_subclass__(
        cls,
        *,
        name: str,
        conftype: type[Config] | None = None,
        **kwargs,
    ):
        super().__init_subclass__(**kwargs)
        cls.name = name
        cls.conftype = conftype

    def on_content_line(self, line: Line, ctx: Substitution) -> None:
        pass

    def before_producers(self, ctx: Substitution) -> Iterable[Line]:
        yield from ()

    def on_produced_line(self, line: Line, ctx: Substitution) -> Iterable[Line]:
        yield line

    def after_producers(self, ctx: Substitution) -> Iterable[Line]:
        yield from ()


# exceptions


@dataclass
class DocsubError(Exception):
    """
    Generic docsub error.
    """

    message: str
    loc: Location | None

    def __str__(self) -> str:
        if self.loc:
            return f'{self.loc.leader()}{self.message}'
        else:
            return self.message


class InvalidCommand(DocsubError):
    """
    Invalid docsub command statement.
    """


class InvalidSubstitution(DocsubError):
    """
    Invalid docsub substitution.
    """


class RuntimeCommandError(DocsubError):
    """
    Runtime docsub command error.
    """


class StopSubstitution(Exception):
    """
    Block substitution stop signal.
    """
