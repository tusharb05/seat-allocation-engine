import asyncio
from app.db.engine import async_engine
from app.db.models import Base
import os

async def main():
    print(os.getenv("DATABASE_URL"))
    print("\n\n\n\n\n\n\n\n\n")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(main())
