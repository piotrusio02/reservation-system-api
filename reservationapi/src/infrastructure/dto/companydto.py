"""A module containing DTO models for output company account."""

from typing import List, Optional

from asyncpg import Record
from pydantic import BaseModel, UUID4, ConfigDict

from src.infrastructure.dto.accountdto import AccountDTO, AccountPublicDTO
from src.infrastructure.dto.categorydto import CategoryDTO

class CompanyDTO(BaseModel):
    """A model representing DTO for company data."""

    id: int
    name: str
    city: str
    postal_code: str
    street: str
    category: CategoryDTO
    description: Optional[str] = None
    account: AccountDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "CompanyDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            CompanyDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            city=record_dict.get("city"),
            postal_code=record_dict.get("postal_code"),
            street=record_dict.get("street"),
            category=CategoryDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1")
            ),
            description=record_dict.get("description"),
            account=AccountDTO(
                id=record_dict.get("id_2"),
                email=record_dict.get("email"),
                phone_number=record_dict.get("phone_number"),
                role=record_dict.get("role")
            )
        )

class CompanyListDTO(BaseModel):
    """A model representing minimum DTO for company data."""

    id: int
    name: str
    city: str
    category: CategoryDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "CompanyListDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            CompanyListDTO: The minimum DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            city=record_dict.get("city"),
            category=CategoryDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1")
            )
        )

class CompanyPublicDTO(BaseModel):
    """A model representing company DTO for user view."""

    id: int
    name: str
    city: str
    postal_code: str
    street: str
    category: CategoryDTO
    description: Optional[str] = None
    account: AccountPublicDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "CompanyPublicDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            CompanyPublicDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            city=record_dict.get("city"),
            postal_code=record_dict.get("postal_code"),
            street=record_dict.get("street"),
            category=CategoryDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1")
            ),
            description=record_dict.get("description"),
            account=AccountPublicDTO(
                phone_number=record_dict.get("phone_number"),
            )
        )

