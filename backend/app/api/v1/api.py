from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.airline import router as airline_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(airline_router)


@api_router.get("/health")
def health_check():
    return {"status": "ok"}
