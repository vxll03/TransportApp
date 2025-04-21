from datetime import timedelta
from fastapi import HTTPException
from src.config.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_user,
    parameters,
)
from src.model.user import User
from src.schema.user_schema import Token, UserCreate, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession


async def user_register(user: UserCreate, db: AsyncSession) -> User:
    db_user = await get_user(db, user.username)
    if db_user:
        raise ValueError("Username already taken")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password, role=user.role)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def user_login(user: UserLogin, db: AsyncSession):
    db_user = await authenticate_user(db, user.username, user.password)
    if not db_user:
        raise ValueError("Username or password incorrect")

    return create_tokens(db_user.username, db_user.role.value)


def create_tokens(username, role) -> Token:
    access_token = create_access_token(
        data={"sub": username, "role": role},
        expires_delta=timedelta(minutes=parameters.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(data={"sub": username, "role": role})
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
