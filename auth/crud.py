from . import models, schemas

async def create(user: schemas.UserCreate) -> models.User:
    user = await models.User.create(**user.dict())
    await user.save()
    return user


async def get(username: str) -> models.User:
    return await models.User.get(username=username)


async def update(user: models.User, update_data: schemas.UserUpdate) -> models.User:
    updated_user = await user.update_from_dict(update_data.dict(exclude_none=True))
    await updated_user.save()
    return updated_user


async def delete(username: str):
    user = await get(username)
    await user.delete()
