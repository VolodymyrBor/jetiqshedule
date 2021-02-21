import datetime

from pydantic import BaseModel

from .enums import VisitStatuses
from lesson_schedule.schemes import LessonInDB


class ScheduledVisit(BaseModel):
    login: str
    password: str
    lesson: LessonInDB
    status: VisitStatuses
    date: datetime.datetime
    error_message: str = None
    visit_start: datetime.datetime = None
    visit_finish: datetime.datetime = None
    owner_id: int
