from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.airline import router as airline_router
from app.api.v1.airport import router as airport_router
from app.api.v1.route import router as route_router
from app.api.v1.flight import router as flight_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(airline_router)
api_router.include_router(airport_router)
api_router.include_router(route_router)
api_router.include_router(flight_router)

@api_router.get("/health")
def health_check():
    return {"status": "ok"}
