"""A module containing DTO models for output user account."""


from pydantic import BaseModel, ConfigDict
from asyncpg import Record

from src.infrastructure.dto.accountdto import AccountDTO, AccountPublicDTO


class UserDTO(BaseModel):
    """A model representing DTO for user data."""

    id: int
    first_name: str
    last_name: str
    account: AccountDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True
    )

    @classmethod
    def from_record(cls, record: Record) -> "UserDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            UserDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            first_name=record_dict.get("first_name"),
            last_name=record_dict.get("last_name"),
            account=AccountDTO(
                id=record_dict.get("id_1"),
                email=record_dict.get("email"),
                phone_number=record_dict.get("phone_number"),
                role=record_dict.get("role")
            )
        )

class UserForCompanyDTO(BaseModel):
    """A model representing user DTO for company view."""
    id: int
    first_name: str
    last_name: str
    account: AccountPublicDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True
    )

    @classmethod
    def from_record(cls, record: Record) -> "UserForCompanyDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            UserForCompanyDTO: The final DTO for company instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            first_name=record_dict.get("first_name"),
            last_name=record_dict.get("last_name"),
            account=AccountPublicDTO(
                phone_number=record_dict.get("phone_number"),
            )
        )