"""Module containing account repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID4

from src.core.domain.account import Account

class IAccountRepository(ABC):
    """An abstract class representing protocol of account repository."""

    @abstractmethod
    async def register_account(self, data: Account) -> Any | None:
        """The abstract creating new account

        Args:
            data (AccountIn): e-mail, password, phone number, role (user or company)

        Returns:
            Any: The newly created account object
        """

    @abstractmethod
    async def get_account_by_uuid(self, account_id: UUID4) -> Any | None:
        """The abstract getting account by provided id.

        Args:
            account_id (uuid): The id of the account.

        Returns:
            Any | None: The account details
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        """The abstract getting account by e-mail.

        Args:
            email (str): The e-mail of the account.

        Returns:
            Any | None: The account details, exist information
        """

    @abstractmethod
    async def update_password(self, account_id: UUID4, new_password: str) -> Any | None:
        """The abstract updating account password.

        Args:
            account_id (uuid): The id of the account.
            new_password (str): The new password

        Returns:
            Any | None: The updated password.
        """