from pydantic import BaseModel
from datetime import date

# what we gonnna send to api while creating a booking
class BookingCreate(BaseModel):
    room_id: int
    guest_name: str
    check_in_date: date
    check_out_date: date


# what api gonna return after post api , in response
class BookingOut(BaseModel):
    id: int
    room_id: int
    guest_name: str
    check_in_date: date
    check_out_date: date

    class Config:
        from_attributes = True
