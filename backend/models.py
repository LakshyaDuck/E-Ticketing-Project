from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Numeric
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# AIRCRAFT
class Aircraft(Base):
    __tablename__ = "aircraft"

    aircraft_id = Column(Integer, primary_key=True)
    model = Column(String(50), nullable=False)
    total_capacity = Column(Integer)

    seats = relationship("Seat", back_populates="aircraft")
    flights = relationship("Flight", back_populates="aircraft")


#AIRLINE
class Airline(Base):
    __tablename__ = "airline"

    airline_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(3))
    price_factor = Column(Numeric(3, 2))

    flights = relationship("Flight", back_populates="airline")


#AIRPORT
class Airport(Base):
    __tablename__ = "airport"

    airport_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)


#ROUTE
class Route(Base):
    __tablename__ = "route"

    route_id = Column(Integer, primary_key=True)
    distance_or_time = Column(Integer)
    base_price = Column(Numeric(10, 2))

    source_airport_id = Column(Integer, ForeignKey("airport.airport_id"))
    destination_airport_id = Column(Integer, ForeignKey("airport.airport_id"))


#FLIGHT
class Flight(Base):
    __tablename__ = "flight"

    flight_id = Column(Integer, primary_key=True)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)

    route_id = Column(Integer, ForeignKey("route.route_id"))
    airline_id = Column(Integer, ForeignKey("airline.airline_id"))
    aircraft_id = Column(Integer, ForeignKey("aircraft.aircraft_id"))

    airline = relationship("Airline", back_populates="flights")
    aircraft = relationship("Aircraft", back_populates="flights")


#CABIN CLASS
class CabinClass(Base):
    __tablename__ = "cabinclass"

    class_id = Column(Integer, primary_key=True)
    class_name = Column(String(50), nullable=False)

    seats = relationship("Seat", back_populates="cabin_class")


#SEAT
class Seat(Base):
    __tablename__ = "seat"

    seat_id = Column(Integer, primary_key=True)
    seat_number = Column(String(10), nullable=False)
    seat_type = Column(String(20))

    aircraft_id = Column(Integer, ForeignKey("aircraft.aircraft_id"))
    class_id = Column(Integer, ForeignKey("cabinclass.class_id"))

    aircraft = relationship("Aircraft", back_populates="seats")
    cabin_class = relationship("CabinClass", back_populates="seats")


#USER
class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone_number = Column(String(20))
    id_number = Column(String(50))
    id_type = Column(String(20))
    email = Column(String(100))
    username = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)

    bookings = relationship("Booking", back_populates="user")


#BOOKING
class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False)
    booking_time = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("user.user_id"))
    flight_id = Column(Integer, ForeignKey("flight.flight_id"))
    seat_id = Column(Integer, ForeignKey("seat.seat_id"))

    from_airport_id = Column(Integer, ForeignKey("airport.airport_id"))
    to_airport_id = Column(Integer, ForeignKey("airport.airport_id"))

    user = relationship("User", back_populates="bookings")

    ticket = relationship("Ticket", uselist=False, back_populates="booking")
    payment = relationship("Payment", uselist=False, back_populates="booking")


#TICKET
class Ticket(Base):
    __tablename__ = "ticket"

    ticket_id = Column(Integer, primary_key=True)
    issued_time = Column(DateTime, nullable=False)

    booking_id = Column(Integer, ForeignKey("booking.booking_id"))

    booking = relationship("Booking", back_populates="ticket")


#PAYMENT
class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    payment_time = Column(DateTime, nullable=False)

    booking_id = Column(Integer, ForeignKey("booking.booking_id"))

    booking = relationship("Booking", back_populates="payment")
