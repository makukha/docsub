from enum import StrEnum
import sys

from loguru import logger

from .__base__ import Config


class LogLevel(StrEnum):
    TRACE = 'TRACE'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    SUCCESS = 'SUCCESS'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class LoggingConfig(Config):
    level: LogLevel | None = None


FORMAT = (
    '<green>{time:YYMMDD HH:mm:ss.S}</green> | '
    '<level>{level: <8}</level> | '
    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'
)


def configure_logging(conf: LoggingConfig) -> None:
    logger.remove()
    if conf.level is not None:
        logger.add(sys.stderr, level=conf.level, format=FORMAT, filter='docsub')
