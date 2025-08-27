# Hotel Booking Backend 

## Problem Statement
This project implements a **hotel booking system** backend.  
You can:
- View hotels and add hotels
- View rooms, room details and add rooms
- Search hotels by city or name efficiently
- Create bookings with concurrency-safe logic to prevent double bookings  

The system uses:
- PostgreSQL as the database for hotels, rooms, and bookings
- Redis for caching frequently accessed data
- In-memory maps for fast hotel search

---

## Approach & Architecture
### Key Components:
1. **Hotels**
   - `POST /hotels` – Create a hotel
   - `GET /hotels` – List all hotels 

2. **Rooms**
   - `POST /rooms` – Create a room
   - `GET /rooms/{room_id}` – Get room details

3. **Bookings**
   - `POST /bookings` – Create a booking

4. **Search**
   - `GET /search` – Search hotels by city and/or hotel name
   - Uses in-memory maps  for O(1) lookups

### Caching Strategy
- **Redis**:
  - Caches hotel list
  - Cache expiration: 5 minutes (300 seconds)
- **Cache invalidation**:
  - On hotel creation → invalidate hotels list cache
  - On room creation → optional invalidation if we cache room lists
  - On booking → invalidate room cache

### Concurrency Handling
- Bookings use **row-level locks** to prevent simultaneous double booking.
- Overlapping date checks ensure no conflicting bookings are created.


---

## Setup Instructions

1. **Clone the repository**
```bash
git clone <repo-url>
cd frnd
```

2. **Install uv**
```bash
pip install uv
```

3. **Start your docker-engine**
```bash
docker-compose up -d
```

4. **Create .env file in root folder**
```bash
DATABASE_URL = "postgresql://user:password@localhost:5433/db"
REDIS_URL="redis://localhost:6379"
```
4. **Migrate data models**
```bash
uv run python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

```
6. **Run the test cases**
```bash
uv run python -m pytest app/ -v
```

7. **Run the Application**
```bash
uv run uvicorn app.main:app --reload
```

8. **Go to localhost:8000/health**
```bash
{"status":"ok"}
```

9. **Access docs**
- Swagger UI: http://127.0.0.1:8000/docs.



---

## Example Requests

1. **Create Hotel**
```bash
POST /hotels
Content-Type: application/json

{
  "name": "Hotel Paradise",
  "city": "Bangalore"
}
```

2. **List Hotels**
```bash
GET /hotels
```

3. **Create Rooms**
```bash
POST /rooms
Content-Type: application/json

{
  "hotel_id": 1,
  "room_type": "double",
  "price": 1200
}
```

4. **Create Booking**
```bash
POST /bookings
Content-Type: application/json

{
  "room_id": 1,
  "guest_name": "Alok Kumar",
  "check_in": "2025-08-26",
  "check_out": "2025-08-28"
}
```


5. **Seach Hotels**
```bash
GET /search?city=Bangalore&name=Hotel%20Paradise

```





### Complex Logic / Trade-offs
- **In-memory search**:
  - Pros: O(1) lookups for city/name
  - Cons: Must reload if DB changes (handled for assignment by using static data)
- **Redis caching**:
  - Improves performance for hot endpoints
  - Cache invalidation is critical to prevent stale data
- **Booking concurrency**:
  - Row-level locks prevent double booking
  - Overlapping date check ensures correctness




  
###  [Watch my Loom video](https://www.loom.com/share/1153c313b8e844f0bd10617f6c75218b?sid=8b52e3d9-7518-45a1-8a6f-9d4e70c339c3)
*Sorry for the voice issue.*
