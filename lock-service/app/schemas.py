from pydantic import BaseModel
from typing import List

class LockRequest(BaseModel):
    show_id: str
    seat_ids: List[str]
    user_id: str


class LockResponse(BaseModel):
    success: bool
    seat_ids: List[str]


class VerifyLockRequest(BaseModel):
    show_id: str
    seat_id: str
    user_id: str