from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import get_db
from src.schema.user_schema import Token, UserCreate, UserLogin
from src.service.auth_service import user_login, user_register


auth = APIRouter()


@auth.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_user = await user_register(user, db)
        return {"message": "User created", "Username": db_user.username}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        token = await user_login(user, db)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
