from typing import List

from fastapi import APIRouter, status

from . import crud
from .shemes import Subject, SubjectUpdate, Lesson, LessonInDB


schedule = APIRouter()


@schedule.get('/subject', response_model=List[Subject], tags=['subjects'])
async def get_all_subjects():
    return await crud.get_all_subjects()


@schedule.put('/subject', response_model=Subject, tags=['subjects'], status_code=status.HTTP_201_CREATED)
async def create_subject(subject: Subject):
    return await crud.create_subject(subject)


@schedule.get('/subject/{name}', response_model=Subject, tags=['subjects'])
async def get_subject(name: str):
    return await crud.get_subject(name)


@schedule.delete('/subject/{name}', tags=['subjects'])
async def delete_subject(name: str):
    await crud.delete_subject(name)
    return {
        'message': 'successfully'
    }


@schedule.patch('/subject/{name}', response_model=Subject, tags=['subjects'])
async def update_subject(name: str, update_data: SubjectUpdate):
    return await crud.update_subject(name, update_data)


@schedule.get('/lesson', response_model=List[LessonInDB], tags=['lessons'])
async def get_all_lessons():
    lessons = await crud.get_all_lessons()
    return lessons


@schedule.get('/lesson/{lesson_id}', response_model=LessonInDB, tags=['lessons'])
async def get_lesson(lesson_id: int):
    return await crud.get_lesson_by_id(lesson_id)


@schedule.put('/lesson', response_model=LessonInDB, tags=['lessons'])
async def create_lesson(lesson: Lesson):
    return await crud.create_lesson(lesson)
