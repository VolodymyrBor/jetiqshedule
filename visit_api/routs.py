from typing import List, Optional

from fastapi import APIRouter

from . import crud, schemes
from lesson_schedule.enums import WeekDays
from shared.shemes import StatusResponse, Statuses

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


@visit_router.get('/visit_statuses/{login}', response_model=List[schemes.VisitInfo], tags=tags)
async def get_visit(login: str, lesson_id: Optional[int] = None):
    visits = await crud.get_visits(login, lesson_id)
    return visits


@visit_router.delete('/visit_status/{visit_id}', response_model=StatusResponse, tags=tags)
async def delete_visit(visit_id: int):
    await crud.delete_visit(visit_id)
    return StatusResponse(status=Statuses.OK)
