import datetime

from pydantic import BaseModel

from .enums import VisitStatuses


class VisitStatus(BaseModel):
    id: int
    status: VisitStatuses
    error_message: str = None
    start = datetime.datetime
    finish = datetime.datetime
