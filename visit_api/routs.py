from typing import List, Optional

from fastapi import APIRouter, Depends

from . import crud, schemes
from auth import User, get_current_user
from lesson_schedule.enums import WeekDays
from shared.shemes import StatusResponse, Statuses

visit_router = APIRouter()
tags = ['visit']


@visit_router.post('/lesson', response_model=schemes.VisitInfo,  tags=tags)
async def visit_lesson(lesson_visit: schemes.LessonVisit, user: User = Depends(get_current_user)):
    visit = await crud.create_visit_for_lesson(lesson_visit, user)
    return visit


@visit_router.post('/lessons', response_model=List[schemes.VisitInfo],  tags=tags)
async def visit_lessons(
        visit_data: schemes.Visit,
        weekday: WeekDays = None,
        week_slug: str = None,
        user: User = Depends(get_current_user),
        ):
    visits = await crud.create_visits(user, visit_data, weekday, week_slug)
    return visits


@visit_router.get('/visit_status/{visit_id}', response_model=schemes.VisitInfo, tags=tags)
async def get_visit(visit_id: int, user: User = Depends(get_current_user)):
    visit = await crud.get_visit(visit_id, user)
    return visit


@visit_router.get('/visit_statuses/', response_model=List[schemes.VisitInfo], tags=tags)
async def get_visits(lesson_id: Optional[int] = None, user: User = Depends(get_current_user)):
    visits = await crud.get_visits(user, lesson_id)
    return visits


@visit_router.delete('/visit_status/{visit_id}', response_model=StatusResponse, tags=tags)
async def delete_visit(visit_id: int, user: User = Depends(get_current_user)):
    await crud.delete_visit(visit_id, user)
    return StatusResponse(status=Statuses.OK)
