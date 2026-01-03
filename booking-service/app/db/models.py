import enum
import uuid
from typing import Optional

from sqlalchemy import (
    Enum,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class SeatStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"


class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    show_id: Mapped[str] = mapped_column(
        index=True,
        nullable=False,
    )
    status: Mapped[SeatStatus] = mapped_column(
        Enum(SeatStatus, name="seat_status"),
        nullable=False,
        default=SeatStatus.AVAILABLE,
    )


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    show_id: Mapped[str] = mapped_column(
        nullable=False,
    )
    seat_id: Mapped[str] = mapped_column(
        ForeignKey("seats.id", ondelete="RESTRICT"),
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        nullable=False,
    )
    request_id: Mapped[str] = mapped_column(
        nullable=False,
    )

    seat: Mapped["Seat"] = relationship(
        lazy="joined",
    )

    __table_args__ = (
        UniqueConstraint("seat_id", "request_id", name="uq_booking_request_seat"),
        UniqueConstraint("show_id", "seat_id", name="uq_show_seat"),
    )
