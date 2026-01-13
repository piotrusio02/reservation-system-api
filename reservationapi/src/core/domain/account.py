"""Module containing account-related domain models"""

from enum import Enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict, UUID4

class Role(Enum):
    """Enum representing possible roles for an account.

    Attributes:
        USER: Regular client.
        COMPANY: Company account with services
    """
    USER = "user"
    COMPANY = "company"

class AccountIn(BaseModel):
    """Model representing account's DTO attributes."""
    email: str
    phone_number: str
    password: str
    role: Role

class LoginIn(BaseModel):
    """Model containing only authentication credentials."""
    email: str
    password: str

class PasswordUpdateIn(BaseModel):
    """Model containing old and new password for update."""
    old_password: str
    new_password: str

class Account(AccountIn):
    """Model representing account's attributes in the database."""
    id: UUID4
    registration_date: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")