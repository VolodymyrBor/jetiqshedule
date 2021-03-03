import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from .enums import VisitStatuses
from lesson_schedule.schemes import LessonInDB


class ScheduledVisit(BaseModel):
    owner_id: int
    lesson: LessonInDB
    status: VisitStatuses
    date: datetime.datetime

    image: Optional[Path] = None
    error_message: Optional[str] = None
    visit_start: Optional[datetime.datetime] = None
    visit_finish: Optional[datetime.datetime] = None
