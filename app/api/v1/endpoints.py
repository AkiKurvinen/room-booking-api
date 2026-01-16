from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.booking import Room, Booking as BookingModel
from app.schemas.booking import BookingCreate, Booking as BookingSchema, Room

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Room Booking API!"}

@router.post("/bookings/", response_model=BookingSchema)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = BookingModel(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/bookings/", response_model=list[BookingSchema])
def read_bookings(db: Session = Depends(get_db)):
    return db.query(BookingModel).all()

@router.get("/rooms/{room_id}/bookings/", response_model=list[BookingSchema])
def read_bookings_for_room(room_id: int, db: Session = Depends(get_db)):
    bookings = db.query(BookingModel).filter(BookingModel.room_id == room_id).all()
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this room")
    return bookings