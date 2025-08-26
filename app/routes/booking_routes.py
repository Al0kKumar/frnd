from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.database import get_db
from app.models.booking import Booking
from app.models.room import Room, RoomStatus
from app.schemas.booking import BookingCreate, BookingOut
from app.core.cache import delete_cache 
from datetime import date

router = APIRouter(prefix="/bookings", tags=["Bookings"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=BookingOut)
@limiter.limit("5/minute")   # rate limiter
def create_booking(booking: BookingCreate, request: Request, db: Session = Depends(get_db)):
    """
    Create a booking with row-level lock to prevent double booking
    under simultaneous requests. Also invalidates room cache.
    """
    try:
        db.begin()

        # Lock the room row for update
        room = db.query(Room).filter(Room.id == booking.room_id).with_for_update().first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        # Check for overlapping bookings
        overlapping = (
            db.query(Booking)
            .filter(
                Booking.room_id == booking.room_id,
                Booking.check_in_date < booking.check_out_date,
                Booking.check_out_date > booking.check_in_date
            )
            .first()
        )

        if overlapping:
            raise HTTPException(status_code=400, detail="Room already booked for these dates")

        # if not then, Create the booking
        new_booking = Booking(
            room_id=booking.room_id,
            guest_name=booking.guest_name,
            check_in_date=booking.check_in_date,
            check_out_date=booking.check_out_date
        )
        db.add(new_booking)

        # update room status
        room.status = RoomStatus.BOOKED

        # commit transaction
        db.commit()
        db.refresh(new_booking)

        # invalidate the cache as status of the room has changed
        try:
            delete_cache(f"room:{room.id}")  
        except Exception as e:
            print(f"Warning: failed to delete room cache: {e}")

        return new_booking

    except:
        db.rollback()  # either everything or nothing 
        raise
