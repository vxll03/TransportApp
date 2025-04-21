from datetime import datetime, timezone
from pydantic import BaseModel, field_validator

from src.model.booking import Booking


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


class RouteResponse(BaseModel):
    title: str
    departure_place: str
    arrival_place: str
    price: float
    departure_date: datetime
    bookings: list[Booking]

    @field_validator("departure_date")
    def serialize_departure_date(cls, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M")


class RouteUpdate(BaseModel):
    price: float

    @field_validator("price")
    def validate_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price cannot be lower than zero")
        return round(value, 2)
