import datetime
from pathlib import Path
from typing import Optional

from visit_scheduler.enums import VisitStatuses

from pydantic import BaseModel


class Visit(BaseModel):
    date: datetime.date = datetime.datetime.now().date()


class LessonVisit(Visit):
    lesson_id: int


class VisitInfo(BaseModel):
    id: int
    lesson_id: int
    date: datetime.date
    status: VisitStatuses
    image: Optional[Path] = None
    error_message: Optional[str] = None
    visit_start: Optional[datetime.datetime] = None
    visit_finish: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True
