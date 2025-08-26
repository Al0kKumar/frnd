from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routes import hotel_routes
from app.routes import room_routes
from app.routes import booking_routes
from app.routes import search_routes
from app.core.database import Base, engine
from app.utils.load_hotels import load_hotels_mock
import app.models  


# db setup
Base.metadata.create_all(bind=engine)

# ratelimiter setup
limiter = Limiter(key_func=get_remote_address)  


app = FastAPI(title="Hotel Booking Platform")
app.state.limiter = limiter

# Exception handler for rate limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Rate limit exceeded. Please try again later."}
    )



app.include_router(hotel_routes.router)
app.include_router(room_routes.router)
app.include_router(booking_routes.router)
app.include_router(search_routes.router)


# for loading mock hotels
load_hotels_mock(num_hotels=1_000_000, num_cities=100)


@app.get("/health")
def health():
    return {"status": "ok"}
