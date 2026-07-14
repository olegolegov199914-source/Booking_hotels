from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router
from app.hotels.rooms.router import router as rooms_router

app = FastAPI()

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router)
app.include_router(rooms_router)
class HotelSearchArgs():
    def __init__(
        self,
        location: str,
        date_from: date,
        date_to: date,
        stars: Optional[int] = Query(None, ge=1, le=5)
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars

@app.get("/hotels")
def get_hotels(search_args: HotelSearchArgs = Depends()):
    return search_args