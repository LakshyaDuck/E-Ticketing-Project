from pydantic import BaseModel


class RouteBase(BaseModel):
    source_airport_id: int
    destination_airport_id: int


class RouteCreate(RouteBase):
    pass


class RouteOut(RouteBase):
    id: int

    class Config:
        from_attributes = True
