from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.hotel import Hotel
from app.schemas.hotel import HotelCreate, HotelOut
from app.core.cache import get_cache, set_cache, delete_cache

router = APIRouter(prefix="/hotels", tags=["Hotels"])

# create a new hotel
@router.post("", response_model=HotelOut)
async def create_hotel(payload: HotelCreate, db: Session = Depends(get_db)):
    """
    Create a new hotel and invalidate the cached hotel list
    to make sure GET /hotels returns the latest data.
    """
    hotel = Hotel(name=payload.name, city=payload.city)
    db.add(hotel)
    db.commit()
    db.refresh(hotel)

    # Invalidate hotels list cache after creating a new hotel
    await delete_cache("hotels:list")

    return HotelOut.from_orm(hotel) 


# list all hotels (caching used)
@router.get("", response_model=list[HotelOut])
async def list_hotels(db: Session = Depends(get_db)):
    """
    Return all hotels, using cache 
    """
    cache_key = "hotels:list"
    cached = await get_cache(cache_key)
    if cached:
        return cached

    hotels = db.query(Hotel).all()
    hotels_serialized = [HotelOut.from_orm(h).dict() for h in hotels]

    await set_cache(cache_key, hotels_serialized, expire_seconds=300)
    return hotels_serialized


# get a single hotel detail by id 
@router.get("/{hotel_id}", response_model=HotelOut)
async def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """
    Return a single hotel by ID.
    """
    cache_key = f"hotel:{hotel_id}"
    cached = await get_cache(cache_key)
    if cached:
        return cached

    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    hotel_serialized = HotelOut.from_orm(hotel).dict()
    await set_cache(cache_key, hotel_serialized, expire_seconds=300)
    return hotel_serialized
