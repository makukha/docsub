from dataclasses import dataclass
from enum import Enum
import sys
from typing import Optional

from loguru import logger

from .__base__ import Config


class LogLevel(str, Enum):
    TRACE = 'TRACE'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    SUCCESS = 'SUCCESS'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


@dataclass
class LoggingConfig(Config):
    level: Optional[LogLevel] = None

    def configure(self) -> None:
        logger.remove()
        if self.level is not None:
            logger.add(sys.stderr, level=self.level, format=FORMAT, filter='docsub')


FORMAT = (
    '<green>{time:YYMMDD HH:mm:ss.S}</green> | '
    '<level>{level: <8}</level> | '
    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'
)
