from fastapi import APIRouter, Depends

from src.config.auth import get_current_user
from src.model.user import User


test = APIRouter()


@test.get("/test")
def base(current_user: User = Depends(get_current_user)):
    return {
        "message": "hello world",
        "username": current_user.username,
        "role": current_user.role.value,
    }
