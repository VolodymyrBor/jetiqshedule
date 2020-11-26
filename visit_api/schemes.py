import datetime

from lesson_schedule.schemes import LessonInDB
from visit_scheduler.enums import VisitStatuses

from pydantic import BaseModel


class Visit(BaseModel):
    login: str
    password: str
    date: datetime.date = datetime.datetime.now().date()


class LessonVisit(Visit):
    lesson_id: int


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
