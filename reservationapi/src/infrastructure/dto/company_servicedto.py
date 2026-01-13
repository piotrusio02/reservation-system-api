"""A model containing company service-related models."""

from typing import Iterable, Optional

from asyncpg import Record
from pydantic import BaseModel, ConfigDict, UUID4

from src.infrastructure.dto.accountdto import AccountPublicDTO
from src.infrastructure.dto.company_subcategorydto import SubcategoryDTO
from src.infrastructure.dto.companydto import CompanyDTO, CategoryDTO, AccountDTO, CompanyPublicDTO


class ServiceListDTO(BaseModel):
    """A model representing DTO for service data."""

    id: int
    subcategory_id: int
    name: str
    price: float
    duration_minutes: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "ServiceListDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ServiceListDTO: The final service list DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            subcategory_id=record_dict.get("subcategory_id"),
            name=record_dict.get("name"),
            price=record_dict.get("price"),
            duration_minutes=record_dict.get("duration_minutes"),
            is_active=record_dict.get("is_active")
        )

class ServiceDTO(BaseModel):
    """A model representing DTO for service data."""

    id: int
    name: str
    price: float
    duration_minutes: int
    description: Optional[str] = None
    is_active: bool
    subcategory: SubcategoryDTO
    company: CompanyDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "ServiceDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ServiceDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            price=record_dict.get("price"),
            duration_minutes=record_dict.get("duration_minutes"),
            description=record_dict.get("description"),
            is_active=record_dict.get("is_active"),
            subcategory=SubcategoryDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1"),
            ),
            company=CompanyDTO(
                id=record_dict.get("id_2"),
                name=record_dict.get("name_2"),
                city=record_dict.get("city"),
                postal_code=record_dict.get("postal_code"),
                street=record_dict.get("street"),
                category=CategoryDTO(
                    id=record_dict.get("id_3"),
                    name=record_dict.get("name_3")
                ),
                description=record_dict.get("description_1"),
                account=AccountDTO(
                    id=record_dict.get("id_4"),
                    email=record_dict.get("email"),
                    phone_number=record_dict.get("phone_number"),
                    role=record_dict.get("role")
                ),
            )
        )

class ServicePublicDTO(BaseModel):
    """A model representing public DTO for service data."""

    id: int
    name: str
    price: float
    duration_minutes: int
    description: Optional[str] = None
    is_active: bool
    subcategory: SubcategoryDTO
    company: CompanyPublicDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "ServicePublicDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ServicePublicDTO: The final public DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            price=record_dict.get("price"),
            duration_minutes=record_dict.get("duration_minutes"),
            description=record_dict.get("description"),
            is_active=record_dict.get("is_active"),
            subcategory=SubcategoryDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1"),
            ),
            company=CompanyPublicDTO(
                id=record_dict.get("id_2"),
                name=record_dict.get("name_2"),
                city=record_dict.get("city"),
                postal_code=record_dict.get("postal_code"),
                street=record_dict.get("street"),
                category=CategoryDTO(
                    id=record_dict.get("id_3"),
                    name=record_dict.get("name_3")
                ),
                description=record_dict.get("description_1"),
                account=AccountPublicDTO(
                    phone_number=record_dict.get("phone_number"),
                ),
            )
        )