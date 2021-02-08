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


class TimeZones(str, Enum):
    UTC = 'UTC'
    UA = 'Europe/Kiev'


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
    TIME_ZONE: TimeZones = TimeZones.UTC

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


class FastAPIUpdate(FastAPI):
    HOST: IPv4Address = None
    PORT: int = None
    RELOAD: bool = None


class SchedulerUpdate(Scheduler):
    BROWSER_HEADLESS: bool = None
    INTERVAL: float = None
    TIME_ZONE: TimeZones = None


class Config(BaseConfig):
    LOG_ROOT_LEVEL: LoggingLevel = None
    LOG_LEVEL: LoggingLevel = None
    FAST_API: FastAPIUpdate = FastAPIUpdate()
    SCHEDULER: SchedulerUpdate = SchedulerUpdate()
