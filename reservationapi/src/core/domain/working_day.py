"""Module containing company working day-related domain models"""

from enum import Enum
from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class WeekDay(Enum):
    """Enum representing days of the week."""
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class WorkingDayIn(BaseModel):
    """Model representing company's working day DTO attributes."""
    day: WeekDay
    opening_time: Optional[time] = Field(default=None, examples=["08:00"])
    closing_time: Optional[time] = Field(default=None, examples=["16:30"])


class WorkingDay(WorkingDayIn):
    """Model representing company's working day attributes in the database."""
    id: int
    company_id: int

    model_config = ConfigDict(from_attributes=True,extra="ignore")
