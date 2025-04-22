from datetime import datetime, timedelta, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exception.auth_exception import credentials_exception, refresh_token_exception
from src.model import User
from src.schema import TokenData

from .database import get_db


# Импорт настроек из .env
class Parameters(BaseSettings):  # Обязательно наследуемся от BaseSettings
    SECRET_KEY: str = Field(
        min_length=32, description="Секретный ключ для подписи токенов"
    )
    ALGORITHM: str = Field(default="HS256", description="Алгоритм подписи токенов")

    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = Field(
        default=10, description="Время жизни access токена в минутах"
    )

    REFRESH_TOKEN_EXPIRE_DAYS: PositiveInt = Field(
        default=7, description="Время жизни refresh токена в днях"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="AUTH_",  # Рекомендуется использовать префиксы
    )


parameters = Parameters()  # type: ignore


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(db: AsyncSession, username: str):
    result = await db.scalar(select(User).where(User.username == username))
    return result


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user or not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    to_encode.update({"type": "access"})

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, parameters.SECRET_KEY, algorithm=parameters.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"type": "refresh"})

    expire = datetime.now(timezone.utc) + timedelta(
        days=parameters.REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, parameters.SECRET_KEY, algorithm=parameters.ALGORITHM
    )

    return encoded_jwt


# Валидация пользователя через Access Token (авторизация)
async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    try:
        token = request.cookies.get("access_token")  # type: ignore
        if not token:
            raise credentials_exception
        payload = jwt.decode(
            token, parameters.SECRET_KEY, algorithms=[parameters.ALGORITHM]
        )

        username: str | None = payload.get("sub")
        role: str | None = payload.get("role")

        if username is None or payload.get("type") != "access":
            raise credentials_exception

        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception

    user = await get_user(db, username=token_data.username)  # type: ignore
    if user is None:
        raise credentials_exception

    return user


# Валидация Refresh Token для обновления Access Token
async def validate_refresh_token(db: AsyncSession, refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token, parameters.SECRET_KEY, algorithms=[parameters.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if not username:
            raise refresh_token_exception

        if payload.get("type") != "refresh":
            raise refresh_token_exception

        user = await get_user(db, username=username)
        if not user:
            raise refresh_token_exception

        return user
    except JWTError:
        raise refresh_token_exception
