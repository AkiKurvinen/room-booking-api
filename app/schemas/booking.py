from pydantic import BaseModel

class BookingBase(BaseModel):
    room_id: int
    start_time: str
    end_time: str

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    bookings: list[Booking] = []

    class Config:
        from_attributes = True