from pydantic import BaseModel, EmailStr
from datetime import datetime


class BookingCreate(BaseModel):
    flight_id: int
    seat_number: str
    passenger_name: str
    passenger_email: EmailStr
    passenger_phone: str
    passenger_id_number: str | None = None
    passenger_id_type: str | None = None
    total_amount: float


class BookingOut(BaseModel):
    id: int
    booking_reference: str
    ticket_number: str | None
    flight_id: int
    seat_number: str
    passenger_name: str
    passenger_email: str
    total_amount: float
    status: str
    booking_time: datetime
    issued_time: datetime | None

    class Config:
        from_attributes = True