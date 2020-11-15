from typing import List

from fastapi import APIRouter, status

from . import crud
from .shemes import Subject


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
