from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum


class RoomStatus(str, PyEnum):
    AVAILABLE = "available"
    BOOKED = "booked"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    room_type = Column(String)
    status = Column(SQLEnum(RoomStatus), default=RoomStatus.AVAILABLE, nullable=False)
    price = Column(Float)

    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room", cascade="all, delete-orphan")
