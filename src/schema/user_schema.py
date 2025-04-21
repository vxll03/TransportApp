from pydantic import BaseModel

from src.model.booking import Booking


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
    role: str = "ROLE_USER"


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


class UserBookings(BaseModel):
    bookings: list[Booking]
