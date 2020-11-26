import datetime

from lesson_schedule.schemes import LessonInDB
from visit_scheduler.enums import VisitStatuses

from pydantic import BaseModel


class BaseVisit(BaseModel):
    login: str
    password: str


class LessonVisit(BaseVisit):
    lesson_id: int
    date: datetime.date = datetime.datetime.now().date()


class VisitInfo(BaseModel):
    id: int
    date: datetime.date
    lesson: LessonInDB
    status: VisitStatuses
    error_message: str = None
    visit_start: datetime.datetime = None
    visit_finish: datetime.datetime = None

    class Config:
        orm_mode = True
