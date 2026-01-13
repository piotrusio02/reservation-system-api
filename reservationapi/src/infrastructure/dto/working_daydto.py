"""A model containing working day-related models."""

from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict

class WorkingDayDTO(BaseModel):
    """A model representing DTO for working day data."""

    id: Optional[int] = None
    day: str
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )