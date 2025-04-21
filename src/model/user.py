from sqlalchemy import String, Enum
from src.config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .enum import UserRole

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)

    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")