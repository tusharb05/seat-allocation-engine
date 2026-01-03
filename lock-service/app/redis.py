from app.config import REDIS_URL
import redis.asyncio as redis

redis_client = redis.from_url(REDIS_URL, decode_responses=True)