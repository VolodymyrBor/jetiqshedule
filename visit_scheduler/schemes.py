import datetime

from pydantic import BaseModel

from .enums import VisitStatuses
from lesson_schedule.schemes import LessonInDB


class VisitStatus(BaseModel):
    id: int
    status: VisitStatuses
    error_message: str = None
    start = datetime.datetime
    finish = datetime.datetime


class ScheduledLesson(BaseModel):
    date: datetime.datetime
    lesson: LessonInDB
    status: VisitStatus
    login: str
    password: str
