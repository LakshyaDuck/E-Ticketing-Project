from pydantic import BaseModel


class AirportBase(BaseModel):
    name: str
    city: str
    country: str
    code: str


class AirportCreate(AirportBase):
    pass


class AirportUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    country: str | None = None
    code: str | None = None


class AirportOut(AirportBase):
    id: int

    class Config:
        from_attributes = True
