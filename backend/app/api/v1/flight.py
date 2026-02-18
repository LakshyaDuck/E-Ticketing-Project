from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.deps_auth import get_current_user
from app.models.flight import Flight
from app.schemas.flight import FlightCreate, FlightOut

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.post("/", response_model=FlightOut)
def create_flight(
    data: FlightCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if data.arrival_time <= data.departure_time:
        raise HTTPException(status_code=400, detail="Arrival must be after departure")

    flight = Flight(**data.model_dump())
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight

@router.post("/", response_model=FlightOut)
def create_flight(
    data: FlightCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if data.arrival_time <= data.departure_time:
        raise HTTPException(status_code=400, detail="Arrival must be after departure")

    flight = Flight(**data.model_dump())
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight

@router.get("/", response_model=list[FlightOut])
def list_flights(db: Session = Depends(get_db)):
    return db.query(Flight).all()

