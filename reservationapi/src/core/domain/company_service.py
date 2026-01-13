"""Module containing company service-related domain models"""

from typing import Optional, Iterable

from pydantic import BaseModel, ConfigDict

class CompanyServiceUpdateIn(BaseModel):
    """Model representing updating service DTO attributes"""
    subcategory_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration_minutes: Optional[int] = None

class CompanyServiceIn(BaseModel):
    """Model representing company service's DTO attributes."""
    subcategory_id: int
    name: str
    description: Optional[str] = None
    price: float
    duration_minutes: int


class CompanyService(CompanyServiceIn):
    """Model representing company service's attributes in the database."""
    id: int
    company_id: int
    is_active: bool = False

    model_config = ConfigDict(from_attributes=True, extra="ignore")
