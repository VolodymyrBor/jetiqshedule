from datetime import datetime

from pydantic import BaseModel

from .enums import WeekDays


class Subject(BaseModel):
    name: str
    teacher: str

    class Config:
        orm_mode = True


class SubjectUpdate(Subject):
    name: str = None
    teacher: str = None


class Lesson(BaseModel):
    id: int
    time: datetime
    weekday: WeekDays
    week_slug: str
    subject: Subject

    class Config:
        orm_mode = True
