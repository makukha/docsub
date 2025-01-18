import rich_click as click
from rich_click import pass_obj as pass_env

from .environment import Environment, pass_env

__version__ = '0.7.1'

__all__ = [
    'Environment',
    'click',
    'pass_env',
]
