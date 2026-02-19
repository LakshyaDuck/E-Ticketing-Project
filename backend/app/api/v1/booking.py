from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
import string
from datetime import datetime

from app.api.deps import get_db
from app.api.deps_auth import get_current_user
from app.models.booking import Booking, BookingStatus
from app.models.flight import Flight
from app.schemas.booking import BookingCreate, BookingOut

router = APIRouter(prefix="/bookings", tags=["Bookings"])


def generate_booking_reference():
    """Generate random 6-character alphanumeric reference"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@router.post("/", response_model=BookingOut)
def create_booking(
        data: BookingCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    # Check if flight exists
    flight = db.query(Flight).filter(Flight.id == data.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    # Check if seat is already booked (CRITICAL: prevents race condition)
    existing_booking = db.query(Booking).filter(
        Booking.flight_id == data.flight_id,
        Booking.seat_number == data.seat_number,
    ).first()

    if existing_booking:
        raise HTTPException(status_code=409, detail=f"Seat {data.seat_number} already booked")

    # Check if seat number is valid (exists in aircraft seat map)
    seat_map = flight.aircraft.seat_map
    valid_seat_numbers = []
    if "rows" in seat_map:
        for row in seat_map["rows"]:
            if "seats" in row:
                for seat in row["seats"]:
                    valid_seat_numbers.append(seat["number"])

    if data.seat_number not in valid_seat_numbers:
        raise HTTPException(status_code=400, detail=f"Invalid seat number: {data.seat_number}")

    # Generate unique booking reference
    booking_ref = generate_booking_reference()
    while db.query(Booking).filter(Booking.booking_reference == booking_ref).first():
        booking_ref = generate_booking_reference()

    # Create booking
    booking = Booking(
        booking_reference=booking_ref,
        user_id=current_user.id,
        flight_id=data.flight_id,
        seat_number=data.seat_number,
        passenger_name=data.passenger_name,
        passenger_email=data.passenger_email,
        passenger_phone=data.passenger_phone,
        passenger_id_number=data.passenger_id_number,
        passenger_id_type=data.passenger_id_type,
        total_amount=data.total_amount,
        status=BookingStatus.CONFIRMED,  # Will change to PENDING once payment is added
        issued_time=datetime.utcnow(),
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@router.get("/", response_model=list[BookingOut])
def list_my_bookings(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    """Get all bookings for current user"""
    return db.query(Booking).filter(Booking.user_id == current_user.id).all()


@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(
        booking_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id,  # Only owner can view
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking