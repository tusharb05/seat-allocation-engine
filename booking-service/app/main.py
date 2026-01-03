from fastapi import FastAPI
from app.booking.router import router as booking_router

app = FastAPI(title="Booking Service")

app.include_router(booking_router)
