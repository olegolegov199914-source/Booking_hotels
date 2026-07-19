from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, Depends
from fastapi.staticfiles import StaticFiles
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as router_pages
from app.images.router import router as router_images


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router)
app.include_router(rooms_router)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(router_images)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","OPTIONS", "DELETE", "PUT", "PUTCH"],
    allow_headers=["Conent-Type", "Set-Cookie","Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization",]
)