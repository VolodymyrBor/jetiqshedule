from enum import Enum
from typing import Optional
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
    HOST: Optional[IPv4Address] = None
    PORT: Optional[int] = None
    RELOAD: Optional[bool] = None


class SchedulerUpdate(Scheduler):
    BROWSER_HEADLESS: Optional[bool] = None
    INTERVAL: Optional[float] = None
    TIME_ZONE: Optional[TimeZones] = None


class Config(BaseConfig):
    LOG_ROOT_LEVEL: LoggingLevel = None
    LOG_LEVEL: LoggingLevel = None
    FAST_API: FastAPIUpdate = FastAPIUpdate()
    SCHEDULER: SchedulerUpdate = SchedulerUpdate()


class MySQLConfig(BaseModel):
    HOST: str = 'localhost'
    PORT: int = 3306
    USERNAME: str = 'root'
    PASSWORD: str = 'root'
    DATABASE: str = 'dev'


class JWTAlgorithms(str, Enum):
    HS256 = 'HS256'
    HS384 = 'HS384'
    HS512 = 'HS512'
    RS256 = 'RS256'
    RS384 = 'RS384'
    RS512 = 'RS512'
    ES256 = 'ES256'
    ES384 = 'ES384'
    ES512 = 'ES512'


class AuthConfig(BaseModel):
    SECRET_KEY: str
    ALGORITHM: JWTAlgorithms
    ACCESS_TOKEN_EXPIRE_MINUTES: int
