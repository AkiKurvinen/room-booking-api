from pydantic import BaseModel, ConfigDict


class BookingBase(BaseModel):
    start_time: str
    end_time: str


class BookingCreate(BookingBase):
    room_id: int


class Booking(BookingBase):
    id: int
    room_id: int

    model_config = ConfigDict(from_attributes=True)


class RoomBase(BaseModel):
    name: str


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int
    bookings: list[Booking] = []

    model_config = ConfigDict(from_attributes=True)
