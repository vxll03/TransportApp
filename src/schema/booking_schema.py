from datetime import datetime, timezone
from pydantic import BaseModel, field_validator

from src.model.enum import State
from src.schema.route_schema import RouteResponse
from src.schema.user_schema import UserResponse


class BookingCreate(BaseModel):
    route_id: int
    user_id: int

    booking_date: datetime = datetime.now(timezone.utc)
    departure_date: datetime

    state: State = State.booked

    @field_validator("departure_date")
    def validate_departure_date(cls, value: datetime) -> datetime:
        if value < datetime.now(timezone.utc):
            raise ValueError("Departure date cannot be in the past")
        return value.replace(microsecond=0)


class BookingResponse(BaseModel):
    id: int
    route: RouteResponse
    user: UserResponse

    booking_date: datetime
    departure_date: datetime

    state: State

    @field_validator("departure_date", "booking_date")
    def serialize_dates(cls, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M")


class BookingUpdate(BaseModel):
    state: State
