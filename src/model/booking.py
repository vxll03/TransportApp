from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Enum
from src.config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.model.enum import State

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))
    route: Mapped["Route"] = relationship("Route", back_populates="bookings")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="bookings")

    booking_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )
    departure_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )

    state: Mapped[State] = mapped_column(Enum(State), default=State.booked)
    