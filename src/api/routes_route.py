from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db

routes = APIRouter()

# @routes.get("/")
# async def get_all_routes(db: AsyncSession = Depends(get_db)):
