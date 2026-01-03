import httpx
from app.config import LOCK_SERVICE_URL

async def verify_lock(show_id: str, seat_id: str, user_id: str) -> bool:
    # print("hi")
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{LOCK_SERVICE_URL}/verify-lock",
                json={
                    "show_id": show_id,
                    "seat_id": seat_id,
                    "user_id": user_id
                },
                timeout=2
            )
            # print("there")
            return res.status_code == 200
    except Exception as e:
        print(e)
        print("ERROR OCCURED IN VERIFYING LOCK")