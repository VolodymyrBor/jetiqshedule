from fastapi import APIRouter

from . import crud, schemes

visit_router = APIRouter()
tags = ['visit']


@visit_router.post('/lesson', response_model=schemes.VisitInfo,  tags=tags)
async def visit_lesson(lesson_visit: schemes.LessonVisit):
    visit = await crud.create_visit_for_lesson(lesson_visit)
    return visit
