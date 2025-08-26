from pydantic import BaseModel
from app.models.room import RoomStatus


# what we gonnna send to api while adding rooms in hotel
class RoomCreate(BaseModel):
    hotel_id: int
    room_type: str
    price: float

# what api gonna return after post api , in response
class RoomOut(BaseModel):
    id: int
    hotel_id: int
    room_type: str
    status: RoomStatus

    price: float

    class Config:
        from_attributes = True
