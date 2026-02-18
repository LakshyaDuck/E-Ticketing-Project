from pydantic import BaseModel


class AirlineBase(BaseModel):
    name: str
    code: str
    price_factor: float = 1.0


class AirlineCreate(AirlineBase):
    pass


class AirlineUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    price_factor: float | None = None


class AirlineOut(AirlineBase):
    id: int

    class Config:
        from_attributes = True
