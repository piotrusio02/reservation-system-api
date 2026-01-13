"""Module containing user account-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4

class UserIn(BaseModel):
    """Model representing user's DTO attributes."""
    first_name: str
    last_name: str

class User(UserIn):
    """Model representing user's attributes in the database."""
    id: int
    account_id: UUID4

    model_config = ConfigDict(from_attributes=True, extra="ignore")

