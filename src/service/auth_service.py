from datetime import timedelta

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_user,
    parameters,
    validate_refresh_token,
)
from src.model.enum import UserRole
from src.model.user import User
from src.schema.user_schema import Token, UserCreate, UserLogin


async def user_register(user: UserCreate, db: AsyncSession) -> User:
    db_user = await get_user(db, user.username)
    if db_user:
        raise ValueError("Username already taken")

    hashed_password = get_password_hash(user.password)

    try:
        role = UserRole(user.role.value)  # Здесь не уверен насчет .value
    except KeyError:
        raise ValueError(f"Invalid role. Must be one of: {[r.name for r in UserRole]}")

    db_user = User(username=user.username, password=hashed_password, role=role)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def user_login(user: UserLogin, db: AsyncSession) -> Token:
    db_user = await authenticate_user(db, user.username, user.password)
    if not db_user:
        raise ValueError("Username or password incorrect")

    return create_tokens(db_user.username, db_user.role, refresh=True)


def create_tokens(username: str, role: UserRole, refresh: bool = False) -> Token:
    access_token = create_access_token(
        data={"sub": username, "role": role.value},
        expires_delta=timedelta(minutes=parameters.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    if refresh:
        refresh_token = create_refresh_token(data={"sub": username, "role": role.value})
    else:
        refresh_token = None

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


async def generate_response(token: Token, refresh: bool = False) -> JSONResponse:
    response = JSONResponse(
        content={"Message": "cookies are generated", "token_type": token.token_type}
    )

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=parameters.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    if refresh:
        response.set_cookie(
            key="refresh_token",
            value=token.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=parameters.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )

    return response


async def perform_login(user: UserLogin, db: AsyncSession) -> JSONResponse:
    token = await user_login(user, db)
    return await generate_response(token, refresh=True)

async def perform_refresh(refresh_token: str, db: AsyncSession) -> JSONResponse:
    user = await validate_refresh_token(db, refresh_token)
    new_tokens = create_tokens(user.username, user.role)
    return await generate_response(new_tokens)