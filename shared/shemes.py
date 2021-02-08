from enum import Enum

from pydantic import BaseModel


class Statuses(str, Enum):
    FAILED = 'failed'
    OK = 'ok'


class StatusResponse(BaseModel):
    status: Statuses
