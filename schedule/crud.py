import datetime
from typing import List

from . import shemes, models


async def get_all_subjects() -> List[models.Subject]:
    return await models.Subject.all()


async def create_subject(subject_data: shemes.Subject) -> models.Subject:
    subject_dict = subject_data.dict()
    subject: models.Subject = await models.Subject.create(**subject_dict)
    return subject


async def get_subject(name: str) -> models.Subject:
    subject = await models.Subject.get(name=name)
    return subject


async def delete_subject(name: str):
    subject = await get_subject(name)
    await subject.delete()


async def update_subject(name: str, update_data: shemes.SubjectUpdate) -> models.Subject:
    subject = await get_subject(name)
    update_dict = update_data.dict(exclude_none=True)
    updated_subject = await subject.update_from_dict(update_dict)
    await updated_subject.save()
    return updated_subject


async def get_all_lessons() -> List[models.Lesson]:
    lessons = await models.Lesson.all().prefetch_related('subject')
    return lessons


async def create_lesson(lesson_data: shemes.Lesson) -> models.Lesson:
    lesson_dict = lesson_data.dict(exclude={'time', 'subject_name'})
    lesson_time = datetime.datetime(
        year=2020,
        month=1,
        day=1,
        hour=lesson_data.time.hour,
        minute=lesson_data.time.minute,
    )
    lesson_dict['time'] = lesson_time
    lesson_dict['subject'] = await get_subject(lesson_data.subject_name)
    lesson: models.Lesson = await models.Lesson.create(**lesson_dict)
    return lesson
