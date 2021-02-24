from typing import List

from . import schemes
from auth import User
from visit_scheduler import models, enums
from lesson_schedule import crud as lesson_crud


async def create_visit_for_lesson(lesson_visit: schemes.LessonVisit, owner: User) -> models.ScheduledVisit:

    lesson = await lesson_crud.get_lesson_by_id(lesson_visit.lesson_id, owner)

    visit = await models.ScheduledVisit.create(
        date=lesson_visit.date,
        lesson=lesson,
        login=owner.jetiq_username,
        password=owner.jetiq_password,
        status=enums.VisitStatuses.CREATED,
        owner=owner,
    )
    return visit


async def create_visits(
        owner: User,
        visit_data: schemes.Visit,
        weekday=None,
        week_slug: str = None
        ) -> List[models.ScheduledVisit]:

    lessons = await lesson_crud.get_lessons(weekday, week_slug)
    visits = [
        await models.ScheduledVisit.create(
            date=visit_data.date,
            lesson=lesson,
            login=owner.jetiq_username,
            password=owner.jetiq_password,
            status=enums.VisitStatuses.CREATED,
            owner=owner,
        )
        for lesson in lessons
    ]
    return visits


async def get_visit(visit_id: int, owner: User) -> models.ScheduledVisit:
    visit = await models.ScheduledVisit.filter(owner=owner).get(id=visit_id).prefetch_related('lesson',
                                                                                              'lesson__subject')
    return visit


async def get_visits(owner: User,  lesson_id: int = None) -> List[models.ScheduledVisit]:
    visits_query = models.ScheduledVisit.filter(owner=owner)

    if lesson_id:
        visits_query = visits_query.filter(lesson_id=lesson_id)

    return await visits_query


async def delete_visit(visit_id: int, owner: User):
    visit = await models.ScheduledVisit.filter(owner=owner).get(id=visit_id)
    await visit.delete()
