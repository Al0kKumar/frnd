import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from fastapi.testclient import TestClient
from app.main import app
from datetime import date
import pytest
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.booking import Booking
from app.core.database import SessionLocal, Base, engine

client = TestClient(app)

# db table ssetup
Base.metadata.create_all(bind=engine)

# booking function with double booking prevention
def book_room(db, room_id, guest_name, check_in, check_out):
    # Prevent overlapping bookings
    overlapping = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.check_in_date < check_out,
        Booking.check_out_date > check_in
    ).first()
    if overlapping:
        return None  # Booking rejected due to overlap

    new_booking = Booking(
        room_id=room_id,
        guest_name=guest_name,
        check_in_date=check_in,
        check_out_date=check_out
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()

# tests
def test_simultaneous_booking(db):
    # create hotel and room
    hotel = Hotel(name="Oceanview", city="Goa")
    db.add(hotel)
    db.commit()
    db.refresh(hotel)

    room = Room(hotel_id=hotel.id, room_type="Single", price=1000)
    db.add(room)
    db.commit()
    db.refresh(room)

    # first booking
    booking1 = book_room(db, room.id, "Guest1", date(2025, 8, 2), date(2025, 8, 4))
    # attempt overlapping booking
    booking2 = book_room(db, room.id, "Guest2", date(2025, 8, 3), date(2025, 8, 4))

    assert booking1 is not None, "first booking should succeed"
    assert booking2 is None, "second booking should fail due to overlap"



def test_booking_edge_case(db):

    # booking with same check-in/check-out date
    hotel = Hotel(name="Mountain Inn", city="Shimla")
    db.add(hotel)
    db.commit()
    db.refresh(hotel)

    room = Room(hotel_id=hotel.id, room_type="Double", price=1500)
    db.add(room)
    db.commit()
    db.refresh(room)

    # booking where check-in == check-out
    booking = book_room(db, room.id, "EdgeCaseGuest", date(2025, 8, 5), date(2025, 8, 5))
    assert booking is not None, "Booking should succeed even for same check-in/check-out"
