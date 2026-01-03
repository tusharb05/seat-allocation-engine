from fastapi import FastAPI, HTTPException, status
from app.services.lock_service import lock_seats, lock_key
from app.schemas import LockRequest, LockResponse, VerifyLockRequest
from app.redis import redis_client

app = FastAPI(title="Seat Locking Service")

@app.post("/seat-lock", response_model=LockResponse)
async def func(req: LockRequest):
    locked = await lock_seats(
        req.show_id,
        req.seat_ids,
        req.user_id
    )
    
    if locked is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat already locked"
        )

    return LockResponse(success=True, seat_ids=locked)


@app.post("/verify-lock")
async def verify_lock(req: VerifyLockRequest):
    key = lock_key(req.show_id, req.seat_id)

    owner = await redis_client.get(key)

    if owner is None:
        # Lock expired or never existed
        raise HTTPException(status_code=409, detail="Lock not found")

    if owner != req.user_id:
        # Lock exists but owned by someone else
        raise HTTPException(status_code=409, detail="Lock not owned by user")

    # Lock exists and is valid
    return {"status": "ok"}