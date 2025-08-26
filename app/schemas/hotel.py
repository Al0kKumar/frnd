from pydantic import BaseModel


# what we gonnna send to api while adding hotel
class HotelCreate(BaseModel):
    name: str
    city: str

# what api gonna return after post api , in response
class HotelOut(BaseModel):
    id: int
    name: str
    city: str

    class Config:
        from_attributes = True
