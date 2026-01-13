"""A module containing account service."""

from abc import ABC, abstractmethod

from pydantic import UUID4

from src.core.domain.account import AccountIn, LoginIn
from src.infrastructure.dto.accountdto import AccountDTO
from src.infrastructure.dto.tokendto import TokenDTO

class IAccountService(ABC):
    """An abstract class for account service."""

    @abstractmethod
    async def register_account(self, account: AccountIn) -> AccountDTO | None:
        """A method registering a new account.

        Args:
            account (AccountIn): The account input data.

        Returns:
            AccountDTO | None: The account DTO model.
        """

    @abstractmethod
    async def authenticate_account(self, account: LoginIn) -> TokenDTO | None:
        """The method authenticating the account.

        Args:
            account (LoginIn): The account data.

        Returns:
            TokenDTO | None: The token details.
        """

    @abstractmethod
    async def update_password(self, uuid: UUID4, old_password: str, new_password: str) -> AccountDTO | None:
        """A method updating password for account.

        Args:
            uuid (UUID4): UUID of the account.
            old_password (str): old password
            new_password (str): new password

        Returns:
            Any | None: The account object if exists.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID4) -> AccountDTO | None:
        """A method getting account by UUID.

        Args:
            uuid (UUID4): The UUID of the account.

        Returns:
            AccountDTO | None: The updated account data, if successful.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> AccountDTO | None:
        """A method getting account by email.

        Args:
            email (str): The email of the account.

        Returns:
            AccountDTO | None: The account data, if found.
        """