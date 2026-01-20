from pydantic import BaseModel


class BookingBase(BaseModel):
    start_time: str
    end_time: str


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: int
    room_id: int  # room_id is still included in the response schema

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
