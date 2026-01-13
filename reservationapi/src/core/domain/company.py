"""Module containing company account-related domain models"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4


class CompanyIn(BaseModel):
    """Model representing company's DTO attributes."""
    name: str
    city: str
    postal_code: str
    street: str
    category_id: int
    description: Optional[str] = None

class Company(CompanyIn):
    """Model representing company's attributes in the database."""
    id: int
    account_id: UUID4

    model_config = ConfigDict(from_attributes=True, extra="ignore")