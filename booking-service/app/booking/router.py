from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.booking.schemas import (
    ConfirmBookingRequest,
    BookingResponse,
    SeatResponse
)
from app.booking.service import confirm_booking
from app.exceptions import LockConflictError

router = APIRouter(prefix="/booking")


@router.post("/confirm", response_model=BookingResponse)
async def confirm(
    req: ConfirmBookingRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await confirm_booking(
            db,
            req.show_id,
            req.seat_ids,
            req.user_id,
            req.request_id,
        )
        return result
    except LockConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # raise HTTPException(status_code=500, detail="Internal booking error")
        print("UNHANDLED EXCEPTION:", e)
        raise



from sqlalchemy import select
from app.db.models import Seat
from typing import List

@router.get(
    "/seats/{show_id}",
    response_model=List[SeatResponse],
)
async def get_seats(
    show_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Seat).where(Seat.show_id == show_id)
    )
    seats = result.scalars().all()
    return seats

