from app.redis import redis_client
from app.schemas import LockRequest, LockResponse
from app.config import LOCK_TTL_SECONDS
from pathlib import Path

LUA_RELEASE_SCRIPT = Path("app/lua/release_lock.lua").read_text()
LUA_ACQUIRE_SCRIPT = Path("app/lua/acquire_locks.lua").read_text()


async def acquire_lock(key: str, user_id: str) -> bool:
    return await redis_client.set(
        key,
        user_id,
        nx=True,
        ex=LOCK_TTL_SECONDS
    )


async def release_lock(key: str, user_id: str):
    await redis_client.eval(
        LUA_RELEASE_SCRIPT,
        1,
        key,
        user_id
    )


def lock_key(show_id: str, seat_id: str) -> str:
    return f"lock:{show_id}:{seat_id}"
    

async def lock_seats(
    show_id: str,
    seat_ids: list[str],
    user_id: str,
):
    keys = [lock_key(show_id, seat_id) for seat_id in seat_ids]

    success = await redis_client.eval(
        LUA_ACQUIRE_SCRIPT,
        len(keys),
        *keys,
        user_id,
        LOCK_TTL_SECONDS,
    )

    if success == 1:
        return seat_ids

    return None

# async def lock_seats(show_id: str, seat_ids: list[str], user_id: str):
#     acquired_seats = []

#     for seat_id in seat_ids:
#         key = lock_key(show_id, seat_id)
#         success = await acquire_lock(key, user_id)

#         if not success:
#             for seat in acquired_seats:
#                 await release_lock(
#                     lock_key(show_id, seat),
#                     user_id
#                 )
#             return None
        
#         acquired_seats.append(seat_id)
    
#     return acquired_seats
            
