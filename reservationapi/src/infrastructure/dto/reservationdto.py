"""A module containing DTO models for output reservations."""

from typing import Optional
from datetime import datetime
from enum import Enum

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from src.infrastructure.dto.accountdto import AccountDTO, AccountPublicDTO
from src.infrastructure.dto.company_subcategorydto import SubcategoryDTO
from src.infrastructure.dto.companydto import CompanyDTO, CompanyPublicDTO
from src.infrastructure.dto.employeedto import EmployeeDTO, EmployeePublicDTO
from src.infrastructure.dto.company_servicedto import ServiceDTO, ServicePublicDTO, ServiceListDTO
from src.infrastructure.dto.userdto import UserDTO, UserForCompanyDTO
from src.infrastructure.dto.categorydto import CategoryDTO


class ReservationStatus(Enum):
    """Enum representing possible statues of a reservation."""
    PENDING = "Pending approval"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

class ReservationListDTO(BaseModel):
    """A model representing DTO for reservation data."""
    id: int
    service: ServiceListDTO
    start_time: datetime
    end_time: datetime
    status: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ReservationListDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReservationListDTO: The final DTO instance.
        """

        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            service=ServiceListDTO(
                id=record_dict.get("id_1"),
                subcategory_id=record_dict.get("subcategory_id"),
                name=record_dict.get("name"),
                price=record_dict.get("price"),
                duration_minutes=record_dict.get("duration_minutes"),
                is_active=record_dict.get("is_active"),
            ),
            start_time=record_dict.get("start_time"),
            end_time=record_dict.get("end_time"),
            status=record_dict.get("status"),
        )

class ReservationDTO(BaseModel):
    """A model representing DTO for reservation data."""

    id: int
    client: Optional[UserForCompanyDTO] = None
    service: ServicePublicDTO
    employee: EmployeePublicDTO
    start_time: datetime
    end_time: datetime
    status: str
    note: Optional[str] = None
    created_date: datetime
    updated_date: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ReservationDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReservationDTO: The final DTO instance.
        """

        record_dict = dict(record)

        client_data = None
        if record_dict.get("id_1") is not None:
            client_data = UserForCompanyDTO(
                id=record_dict.get("id_1"),
                first_name=record_dict.get("first_name"),
                last_name=record_dict.get("last_name"),
                account=AccountPublicDTO(
                    phone_number=record_dict.get("phone_number"),
                )
            )


        return cls(
            id=record_dict.get("id"),
            client=client_data,
            service=ServicePublicDTO(
                id=record_dict.get("id_3"),
                name=record_dict.get("name"),
                price=record_dict.get("price"),
                duration_minutes=record_dict.get("duration_minutes"),
                description=record_dict.get("description"),
                is_active=record_dict.get("is_active"),
                subcategory=SubcategoryDTO(
                    id=record_dict.get("id_4"),
                    name=record_dict.get("name_1"),
                ),
                company=CompanyPublicDTO(
                    id=record_dict.get("id_5"),
                    name=record_dict.get("name_2"),
                    city=record_dict.get("city"),
                    postal_code=record_dict.get("postal_code"),
                    street=record_dict.get("street"),
                    category=CategoryDTO(
                        id=record_dict.get("id_6"),
                        name=record_dict.get("name_3")
                    ),
                    description=record_dict.get("description_1"),
                    account=AccountPublicDTO(
                        phone_number=record_dict.get("phone_number_1"),
                    ),
                ),
            ),
            employee=EmployeePublicDTO(
                id=record_dict.get("id_8"),
                first_name=record_dict.get("first_name_1"),
                last_name=record_dict.get("last_name_1"),
            ),
            start_time=record_dict.get("start_time"),
            end_time=record_dict.get("end_time"),
            status=record_dict.get("status"),
            note=record_dict.get("note"),
            created_date=record_dict.get("created_date"),
            updated_date=record_dict.get("updated_date"),
        )
