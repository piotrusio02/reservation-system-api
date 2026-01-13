"""A model containing account-related models."""

from pydantic import BaseModel, ConfigDict, UUID4


class AccountDTO(BaseModel):
    """A model representing DTO for account data."""

    id: UUID4
    email: str
    phone_number: str
    role: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

class AccountPublicDTO(BaseModel):
    """A model representing DTO for account data."""

    phone_number: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )