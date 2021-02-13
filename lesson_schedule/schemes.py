import datetime as dt
from typing import Optional

from pydantic import BaseModel, validator

from .enums import WeekDays

TIME_FMT = 'HH:MM'


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
    time: dt.time
    weekday: WeekDays
    week_slug: str

    @validator('time', pre=True)
    def to_time(cls, value) -> dt.time:
        if isinstance(value, dt.time):
            return value

        if isinstance(value, dt.datetime, ):
            return value.time()

        try:
            hours, minutes = map(int, value.split(':'))
            time = dt.time(hour=hours, minute=minutes)
        except (ValueError, TypeError):
            raise ValueError(f'Bad format for {value}, expect format: {TIME_FMT}')

        return time


class Lesson(BaseLesson):
    subject_name: str

    class Config:
        orm_mode = True


class LessonInDB(BaseLesson):
    id: int
    subject: Subject

    class Config:
        orm_mode = True


class LessonUpdate(Lesson):
    time: dt.time = None
    subject_name: str = None
    weekday: WeekDays = None
    week_slug: str = None
