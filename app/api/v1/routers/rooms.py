from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Booking
from app.schemas.booking import Booking as BookingSchema
from typing import List

router = APIRouter()


@router.get("/{room_id}/bookings/", response_model=List[BookingSchema])
async def read_bookings_for_room(
    room_id: int, db: Session = Depends(get_db)
) -> List[Booking]:
    bookings = db.query(Booking).filter(Booking.room_id == room_id).all()
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this room")
    return bookings
