from typing import List

from tortoise.exceptions import IntegrityError
from fastapi import APIRouter, status, HTTPException, Depends

from . import crud, enums
from .schemes import Subject, SubjectUpdate, Lesson, LessonInDB, LessonUpdate, SubjectCreate
from auth import User, get_current_user
from shared.shemes import Statuses, StatusResponse

schedule = APIRouter()


@schedule.get('/subject', response_model=List[Subject], tags=['subjects'])
async def get_all_subjects(user: User = Depends(get_current_user)):
    return await user.subjects.filter(owner=user)


@schedule.put('/subject', response_model=Subject, tags=['subjects'], status_code=status.HTTP_201_CREATED)
async def create_subject(subject: Subject, user: User = Depends(get_current_user)):
    subject_to_create = SubjectCreate(**subject.dict(), owner_id=user.pk)
    try:
        created_subject = await crud.create_subject(subject_to_create)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f'Subject with name {subject.name!r} already exists.'
        )

    return created_subject


@schedule.get('/subject/{name}', response_model=Subject, tags=['subjects'])
async def get_subject(name: str, user: User = Depends(get_current_user)):
    return await crud.get_subject(name, user)


@schedule.delete('/subject/{name}', tags=['subjects'], response_model=StatusResponse)
async def delete_subject(name: str, user: User = Depends(get_current_user)):
    await crud.delete_subject(name, user)
    return StatusResponse(status=Statuses.OK)


@schedule.patch('/subject/{name}', response_model=Subject, tags=['subjects'])
async def update_subject(name: str, update_data: SubjectUpdate, user: User = Depends(get_current_user)):
    return await crud.update_subject(name, update_data, user)


@schedule.get('/lesson', response_model=List[LessonInDB], tags=['lessons'])
async def get_lessons(weekday: enums.WeekDays = None, week_slug: str = None, user: User = Depends(get_current_user)):
    lessons = await crud.get_lessons(
        weekday=weekday,
        week_slug=week_slug,
        owner=user,
    )
    return lessons


@schedule.get('/lesson/{lesson_id}', response_model=LessonInDB, tags=['lessons'])
async def get_lesson(lesson_id: int, user: User = Depends(get_current_user)):
    return await crud.get_lesson_by_id(lesson_id, user)


@schedule.put('/lesson', response_model=LessonInDB, tags=['lessons'])
async def create_lesson(lesson: Lesson, user: User = Depends(get_current_user)):
    return await crud.create_lesson(lesson, user)


@schedule.delete('/lesson/{lesson_id}', tags=['lessons'], response_model=StatusResponse)
async def delete_lesson(lesson_id: int, user: User = Depends(get_current_user)):
    await crud.delete_lesson(lesson_id, user)
    return StatusResponse(status=Statuses.OK)


@schedule.patch('/lesson/{lesson_id}', response_model=LessonInDB, tags=['lessons'])
async def update_lesson(lesson_id: int, update_data: LessonUpdate, user: User = Depends(get_current_user)):
    return await crud.update_lesson(lesson_id, update_data, user)


@schedule.post('/lesson/{lesson_id}/copy', response_model=LessonInDB, tags=['lessons'])
async def copy_lesson(lesson_id: int, user: User = Depends(get_current_user)):
    return await crud.copy_lesson(lesson_id, user)
