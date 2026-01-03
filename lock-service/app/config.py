from dotenv import load_dotenv
import os

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

LOCK_TTL_SECONDS = os.getenv("LOCK_TTL_SECONDS", 15)