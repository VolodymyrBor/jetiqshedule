import datetime
from typing import List

from . import schemes, models, enums
from auth import models as auth_models


async def get_all_subjects() -> List[models.Subject]:
    return await models.Subject.all()


async def create_subject(subject_data: schemes.SubjectCreate) -> models.Subject:
    subject_dict = subject_data.dict()
    subject: models.Subject = await models.Subject.create(**subject_dict)
    return subject


async def get_subject(name: str, owner: auth_models.User) -> models.Subject:
    subject = await models.Subject.filter(owner=owner).get(name=name)
    return subject


async def delete_subject(name: str, owner: auth_models.User):
    subject = await get_subject(name, owner)
    await subject.delete()


async def update_subject(name: str, update_data: schemes.SubjectUpdate, owner: auth_models.User) -> models.Subject:
    subject = await get_subject(name, owner)
    update_dict = update_data.dict(exclude_none=True)
    updated_subject = await subject.update_from_dict(update_dict)
    await updated_subject.save()
    return updated_subject


async def get_lessons(
        owner: auth_models.User,
        weekday: enums.WeekDays = None,
        week_slug: str = None
        ) -> List[models.Lesson]:

    lessons = models.Lesson.filter(owner=owner)

    if weekday:
        lessons = lessons.filter(weekday=weekday)

    if week_slug:
        lessons = lessons.filter(week_slug=week_slug)

    return await lessons.prefetch_related('subject')


async def create_lesson(lesson_data: schemes.Lesson, owner: auth_models.User) -> models.Lesson:
    lesson_dict = lesson_data.dict(exclude={'time', 'subject_name'})
    lesson_time = datetime.datetime(
        year=2020,
        month=1,
        day=1,
        hour=lesson_data.time.hour,
        minute=lesson_data.time.minute,
    )
    lesson_dict['time'] = lesson_time
    lesson_dict['subject'] = await get_subject(lesson_data.subject_name, owner=owner)
    lesson: models.Lesson = await models.Lesson.create(**lesson_dict, owner=owner)
    return lesson


async def get_lesson_by_id(lesson_id: int, owner: auth_models.User) -> models.Lesson:
    lesson = await models.Lesson.filter(owner=owner).get(id=lesson_id).prefetch_related('subject')
    return lesson


async def delete_lesson(lesson_id: int, owner: auth_models.User):
    lesson = await get_lesson_by_id(lesson_id, owner)
    await lesson.delete()


async def update_lesson(lesson_id: int, update_date: schemes.LessonUpdate, owner: auth_models.User) -> models.Lesson:
    lesson = await get_lesson_by_id(lesson_id, owner)
    update_dict = update_date.dict(exclude_none=True, exclude={'time', 'subject_name'})
    if update_date.time:
        lesson_time = datetime.datetime(
            year=2020,
            month=1,
            day=1,
            hour=update_date.time.hour,
            minute=update_date.time.minute,
        )
        update_dict['time'] = lesson_time

    if update_date.subject_name:
        update_dict['subject'] = await get_subject(update_date.subject_name, owner)

    updated_lesson = await lesson.update_from_dict(update_dict)
    await updated_lesson.save()
    return updated_lesson


async def copy_lesson(lesson_id: int, owner: auth_models.User) -> models.Lesson:
    lesson = await get_lesson_by_id(lesson_id, owner)
    lesson_data = schemes.Lesson(
        time=lesson.time,
        weekday=lesson.weekday,
        week_slug=lesson.week_slug,
        subject_name=lesson.subject.name,
    )
    return await create_lesson(lesson_data, owner)
