from datetime import datetime
from sqlalchemy import DateTime, Float, String
from src.config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    
    departure_place: Mapped[str] = mapped_column(String)
    arrival_place: Mapped[str] = mapped_column(String)
    
    
    departure_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="route")