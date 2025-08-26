from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    guest_name = Column(String)
    check_in_date = Column(Date)
    check_out_date = Column(Date)

    room = relationship("Room", back_populates="bookings")
