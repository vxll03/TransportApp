from datetime import datetime, timezone
from typing import TYPE_CHECKING, ForwardRef
from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from src.schema.booking_schema import BookingResponse
BookingResponseRef = ForwardRef("BookingResponse")

class RouteCreate(BaseModel):
    title: str
    departure_place: str
    arrival_place: str
    price: float
    departure_date: datetime

    @field_validator("departure_date")
    def validate_departure_date(cls, value: datetime) -> datetime:
        if value < datetime.now(timezone.utc):
            raise ValueError("Departure date cannot be in the past")

        if value.microsecond != 0:
            value = value.replace(microsecond=0)
        return value

    @field_validator("price")
    def validate_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price cannot be lower than zero")
        return round(value, 2)

    @field_validator("title")
    def validate_title_length(cls, value: str) -> str:
        if len(value) > 100:
            raise ValueError("Title must be 100 characters or less")
        return value

    @field_validator("departure_place", "arrival_place")
    def validate_place_length(cls, value: str) -> str:
        if len(value) > 50:
            raise ValueError("Place names must be 50 characters or less")
        return value


class RouteResponse(BaseModel):
    title: str
    departure_place: str
    arrival_place: str
    price: float
    departure_date: str
    bookings: list[BookingResponseRef]

    @field_validator("departure_date")
    def serialize_departure_date(cls, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M")
    
    class Config:
        orm_mode = True


class RouteUpdate(BaseModel):
    price: float

    @field_validator("price")
    def validate_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price cannot be lower than zero")
        return round(value, 2)
