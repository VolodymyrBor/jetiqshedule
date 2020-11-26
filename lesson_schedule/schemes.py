import datetime
from typing import Optional

from pydantic import BaseModel

from .enums import WeekDays


class Subject(BaseModel):
    name: str
    teacher: str
    meet_url_name: Optional[str] = None

    class Config:
        orm_mode = True


class SubjectUpdate(Subject):
    name: str = None
    teacher: str = None
    meet_url_name: str = None


class BaseLesson(BaseModel):
    time: datetime.datetime
    weekday: WeekDays
    week_slug: str


class Lesson(BaseLesson):
    time: datetime.time
    subject_name: str

    class Config:
        orm_mode = True


class LessonInDB(BaseLesson):
    id: int
    subject: Subject

    class Config:
        orm_mode = True


class LessonUpdate(Lesson):
    time: datetime.time = None
    subject_name: str = None
    weekday: WeekDays = None
    week_slug: str = None
