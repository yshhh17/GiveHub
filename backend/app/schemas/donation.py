from pydantic import BaseModel
from datetime import datetime

class DonationCreate(BaseModel):
    amount: int  # in INR

class DonationResponse(BaseModel):
    id: int
    amount: int
    status: bool
    payment_reference: str | None
    created_at: datetime

    class config:
        from_attributes: True

class PayPalOrderResponse(BaseModel):
    order_id: str
    status: str
    approval_url: str | None

class PayPalCaptureRequest(BaseModel):
    order_id: str