from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "USER"


class UserLogin(BaseModel):
    username: str
    password: str
