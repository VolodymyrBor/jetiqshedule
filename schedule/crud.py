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
