import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .models import AuthenticateService
from . import models, schemas, settings, crud
from shared.shemes import Statuses, StatusResponse

TAGS = ['auth']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


auth = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    return await AuthenticateService.get_current_user(token)


@auth.post('/login', response_model=schemas.Token, tags=TAGS)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    try:
        user = await AuthenticateService.authenticate(form_data.username, form_data.password)
    except models.AuthError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthenticateService.create_access_token(
        toke_data=schemas.TokenData(username=user.username),
        expires_delta=access_token_expires,
    )

    return access_token


@auth.get('/user/{username}', response_model=schemas.User, tags=TAGS)
async def get_user(username: str) -> models.User:
    return await crud.get(username)


@auth.put('/user', response_model=schemas.User, tags=TAGS)
async def create_user(user: schemas.UserCreate) -> models.User:
    return await crud.create(user)


@auth.patch('/user', response_model=schemas.User, tags=TAGS)
async def update_user(update_data: schemas.UserUpdate, user: models.User = Depends(get_current_user)) -> models.User:
    return await crud.update(user, update_data)


@auth.delete('/user', response_model=StatusResponse, tags=TAGS)
async def delete_user(user: models.User = Depends(get_current_user)) -> StatusResponse:
    await user.delete()
    return StatusResponse(status=Statuses.OK)
