from fastapi import APIRouter
from app.api.v1.routers import bookings, rooms

api_router = APIRouter()

api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])


@api_router.get("/")
async def read_root() -> dict:
    return {"message": "Room Booking API is running"}
