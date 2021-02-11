from typing import List

from tortoise.exceptions import IntegrityError
from fastapi import APIRouter, status, HTTPException

from . import crud, enums
from shared.shemes import Statuses, StatusResponse
from .schemes import Subject, SubjectUpdate, Lesson, LessonInDB, LessonUpdate


schedule = APIRouter()


@schedule.get('/subject', response_model=List[Subject], tags=['subjects'])
async def get_all_subjects():
    return await crud.get_all_subjects()


@schedule.put('/subject', response_model=Subject, tags=['subjects'], status_code=status.HTTP_201_CREATED)
async def create_subject(subject: Subject):

    try:
        created_subject = await crud.create_subject(subject)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f'Subject with name {subject.name!r} already exists.'
        )

    return created_subject


@schedule.get('/subject/{name}', response_model=Subject, tags=['subjects'])
async def get_subject(name: str):
    return await crud.get_subject(name)


@schedule.delete('/subject/{name}', tags=['subjects'], response_model=StatusResponse)
async def delete_subject(name: str):
    await crud.delete_subject(name)
    return StatusResponse(status=Statuses.OK)


@schedule.patch('/subject/{name}', response_model=Subject, tags=['subjects'])
async def update_subject(name: str, update_data: SubjectUpdate):
    return await crud.update_subject(name, update_data)


@schedule.get('/lesson', response_model=List[LessonInDB], tags=['lessons'])
async def get_lessons(weekday: enums.WeekDays = None, week_slug: str = None):
    lessons = await crud.get_lessons(
        weekday=weekday,
        week_slug=week_slug,
    )
    return lessons


@schedule.get('/lesson/{lesson_id}', response_model=LessonInDB, tags=['lessons'])
async def get_lesson(lesson_id: int):
    return await crud.get_lesson_by_id(lesson_id)


@schedule.put('/lesson', response_model=LessonInDB, tags=['lessons'])
async def create_lesson(lesson: Lesson):
    return await crud.create_lesson(lesson)


@schedule.delete('/lesson/{lesson_id}', tags=['lessons'], response_model=StatusResponse)
async def delete_lesson(lesson_id: int):
    await crud.delete_lesson(lesson_id)
    return StatusResponse(status=Statuses.OK)


@schedule.patch('/lesson/{lesson_id}', response_model=LessonInDB, tags=['lessons'])
async def update_lesson(lesson_id: int, update_data: LessonUpdate):
    return await crud.update_lesson(lesson_id, update_data)
