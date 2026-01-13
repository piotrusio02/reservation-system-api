"""Module containing company reservation-related domain models"""

from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class ReservationStatus(Enum):
    """Enum representing possible statues of a reservation."""
    PENDING = "Pending approval"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

class ReservationIn(BaseModel):
    """Model representing reservation's DTO attributes."""
    service_id: int
    employee_id: int
    start_time: datetime = Field(..., examples=["2026-01-14T17:30:00"])
    note: Optional[str] = None

class ReservationBroker(ReservationIn):
    """A broker class including system data in the model."""
    client_id: Optional[int] = None
    company_id: int
    end_time: datetime
    status: ReservationStatus
    created_date: datetime
    updated_date: Optional[datetime] = None

class Reservation(ReservationBroker):
    """Model representing reservation's attributes in the database."""
    id: int


class ReservationStatusUpdateIn(BaseModel):
    """Model representing status update for existing reservation"""
    status: ReservationStatus




    model_config = ConfigDict(from_attributes=True, extra="ignore")
