from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.room import Room, RoomStatus
from app.schemas.room import RoomCreate, RoomOut
from app.models.hotel import Hotel
from app.core.cache import get_cache, set_cache, delete_cache

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# create a new room in a hotel
@router.post("/", response_model=RoomOut)
async def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """
    Create a new room. 
    """
    hotel = db.query(Hotel).filter(Hotel.id == room.hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    new_room = Room(
        hotel_id=room.hotel_id,
        room_type=room.room_type,
        price=room.price,
        status=RoomStatus.AVAILABLE
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return RoomOut.from_orm(new_room)

# get room by id (caching used)
@router.get("/{room_id}", response_model=RoomOut)
async def get_room(room_id: int, db: Session = Depends(get_db)):
    """
    Return a single room by ID. 
    """
    cache_key = f"room:{room_id}"
    cached = await get_cache(cache_key)
    if cached:
        return cached

    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    room_serialized = RoomOut.from_orm(room).dict()
    await set_cache(cache_key, room_serialized, expire_seconds=300)
    return room_serialized
