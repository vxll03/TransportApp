from typing import TYPE_CHECKING, ForwardRef

from pydantic import BaseModel, field_validator, model_validator

from src.model.enum import UserRole

if TYPE_CHECKING:
    from src.schema.booking_schema import BookingResponse
BookingResponseRef = ForwardRef("BookingResponse")


class Token(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.USER

    @field_validator("username")
    def username_validate(cls, value: str) -> str:
        if len(value) > 100:
            raise ValueError("Username too long")
        if len(value) < 4:
            raise ValueError("Username too short")
        return value

    @field_validator("password")
    def pass_validate(cls, value: str) -> str:
        if len(value) > 100:
            raise ValueError("Password too long")
        if len(value) < 8:
            raise ValueError("Password too short")
        return value

    @model_validator(mode="after")
    def credentials_validate(self) -> "UserCreate":
        if self.username == self.password:
            raise ValueError("Password cannot match username")
        return self


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole


class UserBookings(BaseModel):
    bookings: list[BookingResponseRef]
