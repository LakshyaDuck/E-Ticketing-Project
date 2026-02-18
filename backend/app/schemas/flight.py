from pydantic import BaseModel
from datetime import datetime


class FlightBase(BaseModel):
    airline_id: int
    route_id: int
    departure_time: datetime
    arrival_time: datetime
    base_price: float
    total_seats: int


class FlightCreate(FlightBase):
    pass


class FlightOut(FlightBase):
    id: int

    class Config:
        from_attributes = True
