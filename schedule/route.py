from typing import List

from fastapi import APIRouter, status

from shemes import Subject


schedule = APIRouter()


subjects_list = [
    Subject(name='English', teacher='Maral'),
    Subject(name='Math', teacher='Vova'),
]


@schedule.get('/', response_model=List[Subject], tags=['subjects'])
async def subjects():
    return subjects_list


@schedule.put('/', response_model=Subject, tags=['subjects'], status_code=status.HTTP_201_CREATED)
async def create_subject(subject: Subject):
    subjects_list.append(subject)
    return subject
