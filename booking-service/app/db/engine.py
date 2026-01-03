from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,         # logging is false
    future=True,
    pool_size=5,
    max_overflow=10,
)
