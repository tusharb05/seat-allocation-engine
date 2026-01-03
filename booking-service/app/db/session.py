from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import async_engine
from sqlalchemy.orm import sessionmaker

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session