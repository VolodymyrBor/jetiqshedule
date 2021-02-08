from typing import List

from fastapi import APIRouter

from . import crud, schemes
from lesson_schedule.enums import WeekDays
from lesson_schedule import crud as lesson_crud


visit_router = APIRouter()
tags = ['visit']


@visit_router.post('/lesson', response_model=schemes.VisitInfo,  tags=tags)
async def visit_lesson(lesson_visit: schemes.LessonVisit):
    visit = await crud.create_visit_for_lesson(lesson_visit)
    return visit


@visit_router.post('/lessons', response_model=List[schemes.VisitInfo],  tags=tags)
async def visit_lessons(visit_data: schemes.Visit, weekday: WeekDays = None, week_slug: str = None):
    visits = await crud.create_visits(visit_data, weekday, week_slug)
    return visits


@visit_router.get('/visit_status/{visit_id}', response_model=schemes.VisitInfo, tags=tags)
async def get_visit(visit_id: int):
    visit = await crud.get_visit(visit_id)
    return visit


@visit_router.get('/visit_status/user/{login}', response_model=List[schemes.VisitInfo], tags=tags)
async def get_visit(login: str):
    visits = await crud.get_visits(login)
    return visits
