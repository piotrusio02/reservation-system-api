"""Module containing company employee-related domain models"""

from pydantic import BaseModel, ConfigDict

class EmployeeIn(BaseModel):
    """Model representing company employee's DTO attributes."""
    first_name: str
    last_name: str
    email: str
    phone_number: str

class Employee(EmployeeIn):
    """Model representing company employee's attributes in the database."""
    id: int
    company_id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
