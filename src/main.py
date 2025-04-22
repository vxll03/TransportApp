from fastapi import FastAPI

from src.api.auth_route import auth
from src.api.test import test

app = FastAPI()
prefix = "/api/v1"

# Авторизация
app.include_router(auth, prefix=f"{prefix}/auth", tags=["auth"])

# Тестовый поинт
app.include_router(test, prefix=prefix, tags=["test"])
