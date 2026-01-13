"""A module containing user service."""

from abc import ABC, abstractmethod

from pydantic import UUID4

from src.core.domain.user import UserIn
from src.infrastructure.dto.userdto import UserDTO

class IUserService(ABC):
    """An abstract class for user service."""

    @abstractmethod
    async def create_user(self, account_id: UUID4, user: UserIn) -> UserDTO | None:
        """A method create a new user.

        Args:
            account_id (UUID4): The account id of the user.
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO model.
        """

    @abstractmethod
    async def get_by_account_id(self, account_id: UUID4) -> UserDTO | None:
        """A method getting user by account id.

        Args:
            account_id (UUID4): The account id of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserDTO | None:
        """A method getting user by account id.

        Args:
            user_id (int): The id of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

    @abstractmethod
    async def update_user(self, account_id: UUID4, data: UserIn) -> UserDTO | None:
        """The method updating user data in the data storage.

        Args:
            account_id (UUID4): The id of the user.
            data (UserIn): The details of the updated user info.

        Returns:
            UserDTO | None: The updated user details.
        """