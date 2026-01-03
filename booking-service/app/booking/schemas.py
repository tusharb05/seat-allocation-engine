from pydantic import BaseModel
from typing import List
from app.db.models import SeatStatus

class ConfirmBookingRequest(BaseModel):
    show_id: str
    seat_ids: List[str]
    user_id: str
    request_id: str


class BookingResponse(BaseModel):
    success: bool
    message: str
    booked_seats: List[str] = []

class SeatResponse(BaseModel):
    id: str
    show_id: str
    status: SeatStatus

    class Config:
        from_attributes = True