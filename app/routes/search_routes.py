from fastapi import APIRouter, Query, Request
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.schemas.hotel import HotelOut
from app.utils.load_hotels import hotels_list, city_map, name_map


router = APIRouter(prefix="/search", tags=["Search"])

limiter = Limiter(key_func=get_remote_address)

# search via hotel name / city
@router.get("/", response_model=List[HotelOut])
@limiter.limit("10/second")  # rate limiter
def search_hotels(
    request: Request,
    city: str = Query(None, description="Filter hotels by city"),
    name: str = Query(None, description="Filter hotels by exact hotel name"),
    limit: int = Query(50, description="Max number of hotels to return")
):
    """
    search hotels efficiently using in-memory data structures.

    Search logic:
    1. both city and name provided: Filter city-hotels by name.
    2. only city provided: Fetch hotels from city_map O(1).
    3. only name provided: Fetch hotels from name_map O(1).
    4. no filters provided: Return first 50 hotels from full hotels_list.

    """

    # both city and name
    if city and name:
        city_hotels = city_map.get(city.lower(), [])
        results = [h for h in city_hotels if h.name.lower() == name.lower()]

    #  only city
    elif city:
        results = city_map.get(city.lower(), [])

    #  only name
    elif name:
        results = name_map.get(name.lower(), [])

    # no filters
    else:
        results = hotels_list

    # return up to limit entries
    return results[:limit]
