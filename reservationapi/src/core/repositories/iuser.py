"""Module containing user repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID4

from src.core.domain.user import UserIn

class IUserRepository(ABC):
    """An abstract class representing protocol of user repository."""

    @abstractmethod
    async def create_user(self, account_id: UUID4, data: UserIn) -> Any | None:
        """The abstract creating new user

        Args:
            account_id (UUID4): The UUID4 of the account.
            data (UserIn): account_id, First name, Last name

        Returns:
            Any: The newly created user object
        """

    @abstractmethod
    async def get_by_account_id(self, account_id: UUID4) -> Any | None:
        """The abstract getting user by provided account id.

        Args:
            account_id (UUID4): The UUID4 of the account.

        Returns:
            Any | None: The user account details
        """

    @abstractmethod
    async def get_by_id(self, id: int) -> Any | None:
        """The abstract getting user by provided id.

        Args:
            id (int): The id of the user.

        Returns:
            Any | None: The user account details
        """

    @abstractmethod
    async def update_user(self, account_id: UUID4, data: UserIn) -> Any | None:
        """The abstract updating user information.

        Args:
            account_id (UUID4): The id of the user.
            data (UserIn): The new user information

        Returns:
            Any | None: The updated user.
        """
