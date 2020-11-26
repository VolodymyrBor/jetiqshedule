from . import schemes
from lesson_schedule import crud as lesson_crud
from visit_scheduler import models, enums


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
