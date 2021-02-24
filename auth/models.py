import datetime as dt
from typing import Optional

from jose import jwt, JWTError
from tortoise import models, fields
from pydantic import ValidationError
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

from .schemas import Token, TokenType, TokenData
from .settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import visit_scheduler
from lesson_schedule.models import Subject, Lesson


class AuthError(Exception):
    pass


class PasswordVerifyError(AuthError):
    pass


class UsernameVerifyError(AuthError):
    pass


class CredentialError(AuthError):
    pass


class AuthenticateService:

    _pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls._pwd_context.verify(password, hashed_password)

    @classmethod
    def create_password_hash(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    @classmethod
    def create_access_token(cls, toke_data: TokenData, expires_delta: Optional[dt.timedelta] = None) -> Token:
        to_encode = toke_data.dict(exclude_none=True)

        if expires_delta:
            expire = dt.datetime.utcnow() + expires_delta
        else:
            expire = dt.datetime.utcnow() + dt.timedelta(minutes=15)

        # TODO add expire to token
        # to_encode['expire'] = expire

        jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        token = Token(access_token=jwt_token, token_type=TokenType.BEARER)
        return token

    @classmethod
    async def authenticate(cls, username: str, password: str) -> 'User':

        try:
            user = await User.get(username=username)
        except DoesNotExist:
            raise UsernameVerifyError(f'Username {username} does not exist')

        if not cls.verify_password(password, user.hashed_password):
            raise PasswordVerifyError('Wrong password')

        return user

    @staticmethod
    async def get_current_user(token: str) -> 'User':
        credentials_exception = CredentialError('Wrong credentials')

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token_data = TokenData(**payload)
        except (JWTError, ValidationError):
            raise credentials_exception

        try:
            user = await User.get(username=token_data.username)
        except DoesNotExist:
            raise credentials_exception

        return user


class User(models.Model):

    # relations
    lessons: models.QuerySet[Lesson]
    subjects: models.QuerySet[Subject]
    visits: models.QuerySet['visit_scheduler.models.ScheduledVisit']

    username = fields.CharField(max_length=100, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=512)
    jetiq_username = fields.CharField(max_length=100)
    jetiq_password = fields.CharField(max_length=100)

    def __init__(self, username: str, email: str, password: str, jetiq_username: str, jetiq_password: str):
        super().__init__(username=username, email=email, jetiq_username=jetiq_username, jetiq_password=jetiq_password)
        self.set_password(password)

    @property
    def password(self) -> str:
        return self.hashed_password

    @password.setter
    def password(self, plain_password: str):
        self.set_password(plain_password)

    def set_password(self, password: str):
        self.hashed_password = AuthenticateService.create_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return AuthenticateService.verify_password(
            password=password,
            hashed_password=self.hashed_password,
        )

    def create_access_token(self) -> Token:
        return AuthenticateService.create_access_token(
            toke_data=TokenData(username=self.username),
            expires_delta=dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    def __str__(self):
        return self.username
