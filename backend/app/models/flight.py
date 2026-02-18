from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.db.base import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)

    airline_id = Column(Integer, ForeignKey("airlines.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)

    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)

    base_price = Column(Float, nullable=False)
    total_seats = Column(Integer, nullable=False)

    airline = relationship("Airline")
    route = relationship("Route")
