"""Module containing company category-related domain models"""

from pydantic import BaseModel, ConfigDict

class Category(BaseModel):
    """Model representing category attributes in the database."""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True, extra="ignore")