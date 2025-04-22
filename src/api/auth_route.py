from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.config.logger import logger
from src.exception.auth_exception import refresh_token_exception
from src.schema.user_schema import (
    Token,
    UserCreate,
    UserLogin,
)
from src.service.auth_service import perform_login, perform_refresh, user_register

auth = APIRouter()


@auth.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_user = await user_register(user, db)

        logger.info(f"New user registered with name {db_user.username}")
        return {"message": "User created", "Username": db_user.username}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"User {user.username} logged in")
        return await perform_login(user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth.post("/refresh", response_model=Token)
async def refresh(request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise refresh_token_exception

    try:
        return await perform_refresh(refresh_token, db)
    except JWTError:
        raise refresh_token_exception


@auth.post("/logout")
async def logout():
    response = JSONResponse(content={"Message": "Logged out successfully"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
