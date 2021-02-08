from typing import List

from . import schemes
from visit_scheduler import models, enums
from lesson_schedule import crud as lesson_crud


async def create_visit_for_lesson(lesson_visit: schemes.LessonVisit) -> models.ScheduledVisit:

    lesson = await lesson_crud.get_lesson_by_id(lesson_visit.lesson_id)

    visit = await models.ScheduledVisit.create(
        date=lesson_visit.date,
        lesson=lesson,
        login=lesson_visit.login,
        password=lesson_visit.password,
        status=enums.VisitStatuses.CREATED,
    )
    return visit


async def create_visits(visit_data: schemes.Visit, weekday=None, week_slug: str = None) -> List[models.ScheduledVisit]:
    lessons = await lesson_crud.get_lessons(weekday, week_slug)
    visits = [
        await models.ScheduledVisit.create(
            date=visit_data.date,
            lesson=lesson,
            login=visit_data.login,
            password=visit_data.password,
            status=enums.VisitStatuses.CREATED,
        )
        for lesson in lessons
    ]
    return visits


async def get_visit(visit_id: int) -> models.ScheduledVisit:
    visit = await models.ScheduledVisit.get(id=visit_id).prefetch_related('lesson', 'lesson__subject')
    return visit


async def get_visits(login: str) -> List[models.ScheduledVisit]:
    visits = await models.ScheduledVisit.filter(login=login)
    return visits


async def delete_visit(visit_id: int):
    visit = await models.ScheduledVisit.get(id=visit_id)
    await visit.delete()
