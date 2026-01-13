"""A model containing employee-related models."""

from pydantic import BaseModel, ConfigDict

class EmployeeDTO(BaseModel):
    """A model representing DTO for employee data."""

    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

class EmployeePublicDTO(BaseModel):
    """A model representing DTO for employee for client data."""

    id: int
    first_name: str
    last_name: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
