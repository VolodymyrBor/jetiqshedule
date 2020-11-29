from enum import Enum
from ipaddress import IPv4Address

from pydantic import BaseModel, validator


class LoggingLevel(str, Enum):
    CRITICAL = 'CRITICAL'
    FATAL = 'FATAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    NOTSET = 'NOTSET'


class FastAPI(BaseModel):
    HOST: IPv4Address
    PORT: int
    RELOAD: bool

    @validator('PORT')
    def port_validator(cls, port: int) -> int:
        if 0 < port <= 65535:
            return port

        raise ValueError('Port must be in 1-65535 range.')


class Scheduler(BaseModel):
    BROWSER_HEADLESS: bool
    INTERVAL: float

    @validator('INTERVAL')
    def interval_validator(cls, interval: float) -> float:
        if 1 < interval <= 60 * 60:
            return interval

        raise ValueError('Interval must be in 1-3600(1 hour) range.')


class BaseConfig(BaseModel):
    LOG_ROOT_LEVEL: LoggingLevel
    LOG_LEVEL: LoggingLevel
    FAST_API: FastAPI
    SCHEDULER: Scheduler


class Config(BaseConfig):
    LOG_ROOT_LEVEL: LoggingLevel = None
    LOG_LEVEL: LoggingLevel = None
    FAST_API: FastAPI = None
    SCHEDULER: Scheduler = None
