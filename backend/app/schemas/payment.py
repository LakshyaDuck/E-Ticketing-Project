from pydantic import BaseModel
from datetime import datetime


class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    currency: str = "USD"
    payment_method: str
    card_number: str  # We'll validate and store only last 4
    card_expiry: str
    card_cvv: str


class PaymentOut(BaseModel):
    id: int
    booking_id: int
    amount: float
    currency: str
    payment_method: str
    card_last4: str | None
    card_brand: str | None
    transaction_id: str | None
    status: str
    failure_reason: str | None
    payment_time: datetime

    class Config:
        from_attributes = True