import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import async_engine
from app.db.models import Seat, SeatStatus


SHOW_ID = "show_1"


SEAT_IDS = [
    "A1", "A2", "A3", "A4", "A5",
    "B1", "B2", "B3", "B4", "B5",
]


async def seed_seats():
    async with AsyncSession(async_engine) as session:
        async with session.begin():

            # Fetch existing seats for this show
            result = await session.execute(
                select(Seat.id).where(Seat.show_id == SHOW_ID)
            )
            existing = {row[0] for row in result.all()}

            new_seats = [
                Seat(
                    id=seat_id,
                    show_id=SHOW_ID,
                    status=SeatStatus.AVAILABLE,
                )
                for seat_id in SEAT_IDS
                if seat_id not in existing
            ]

            if not new_seats:
                print("Seat seed: nothing to insert")
                return

            session.add_all(new_seats)
            print(f"Seat seed: inserted {len(new_seats)} seats")


async def main():
    await seed_seats()


if __name__ == "__main__":
    asyncio.run(main())
