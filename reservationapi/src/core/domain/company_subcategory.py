"""Module containing company service subcategory-related domain models"""

from pydantic import BaseModel, ConfigDict

class SubcategoryIn(BaseModel):
    """Model representing subcategory service's DTO attributes."""
    name: str

class Subcategory(SubcategoryIn):
    """Model representing subcategory service's attributes in the database."""
    id: int
    company_id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

