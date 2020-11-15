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
