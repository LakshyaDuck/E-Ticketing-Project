from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.deps_auth import get_current_user
from app.models.route import Route
from app.schemas.route import RouteCreate, RouteOut

router = APIRouter(prefix="/routes", tags=["Routes"])

@router.post("/", response_model=RouteOut)
def create_route(
    data: RouteCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if data.source_airport_id == data.destination_airport_id:
        raise HTTPException(status_code=400, detail="Source and destination cannot be same")

    route = Route(**data.model_dump())
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

@router.get("/", response_model=list[RouteOut])
def list_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()

