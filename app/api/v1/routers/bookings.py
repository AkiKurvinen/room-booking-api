from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Booking
from app.models.room import Room
from app.schemas.booking import BookingCreate

router = APIRouter()


@router.post("/", response_model=BookingCreate)
async def create_booking_for_room(
    booking: BookingCreate, db: Session = Depends(get_db)
) -> Booking:
    # Ensure the room exists
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Ensure the booking time is not in the past
    if booking.start_time < datetime.now().isoformat():
        raise HTTPException(
            status_code=400, detail="Booking time cannot be in the past"
        )

    # Ensure the end time is not before the start time
    if booking.end_time <= booking.start_time:
        raise HTTPException(
            status_code=400, detail="End time cannot be before or equal to start time"
        )

    # Check for overlapping bookings
    overlapping_booking = (
        db.query(Booking)
        .filter(
            Booking.room_id == booking.room_id,
            Booking.start_time < booking.end_time,
            Booking.end_time > booking.start_time,
        )
        .first()
    )

    if overlapping_booking:
        raise HTTPException(
            status_code=400, detail="Booking times overlap with an existing booking"
        )

    # Create the booking tied to the room
    db_booking = Booking(
        start_time=booking.start_time,
        end_time=booking.end_time,
        room_id=booking.room_id,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.delete("/{booking_id}", status_code=200)
async def delete_booking(booking_id: int, db: Session = Depends(get_db)) -> dict:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}
