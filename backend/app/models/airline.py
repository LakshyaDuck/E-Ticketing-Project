from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base


class Airline(Base):
    __tablename__ = "airlines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    price_factor = Column(Float, default=1.0)
