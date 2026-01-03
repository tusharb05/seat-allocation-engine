from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Seat, Booking, SeatStatus
from app.redis_client import verify_lock
from app.exceptions import LockConflictError
from typing import List

async def confirm_booking(
    session: AsyncSession,
    show_id: str,
    seat_ids: list[str],
    user_id: str,
    request_id: str
):
    
    for seat_id in seat_ids:
        ok = await verify_lock(show_id, seat_id, user_id)
        if not ok:
            raise LockConflictError("Lock expired or not owned")

    result_payload = None

    
    async with session.begin():

        existing_q = await session.execute(
            select(Booking).where(Booking.request_id == request_id)
        )
        existing = existing_q.scalars().all()
        if existing:
            result_payload = {
                "success": True,
                "message": "Booking already confirmed",
                "booked_seats": [b.seat_id for b in existing],
            }
        else:
            stmt = (
                select(Seat)
                .where(
                    Seat.show_id == show_id,
                    Seat.id.in_(seat_ids),
                )
                .with_for_update()
            )
            result = await session.execute(stmt)
            seats = result.scalars().all()

            if len(seats) != len(seat_ids):
                raise ValueError("One or more seats do not exist")

            for seat in seats:
                if seat.status != SeatStatus.AVAILABLE:
                    raise ValueError("Seat already booked")

            for seat in seats:
                seat.status = SeatStatus.BOOKED
                session.add(
                    Booking(
                        show_id=show_id,
                        seat_id=seat.id,
                        user_id=user_id,
                        request_id=request_id,
                    )
                )

            result_payload = {
                "success": True,
                "message": "Booking confirmed",
                "booked_seats": seat_ids,
            }

    return result_payload