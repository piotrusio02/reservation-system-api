"""A module containing user service."""

from pydantic import UUID4

from src.core.domain.user import UserIn
from src.core.repositories.iuser import IUserRepository
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.iuser import IUserService

class UserService(IUserService):
    """An abstract class for user service."""

    _repository: IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    async def create_user(self, account_id: UUID4, user: UserIn) -> UserDTO | None:
        """A method create a new user.

        Args:
            account_id (UUID4): The account id of the user.
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO model.
        """

        user_data = await self._repository.create_user(account_id, user)

        if not user_data:
            return None

        return UserDTO.from_record(user_data)

    async def get_by_account_id(self, account_id: UUID4) -> UserDTO | None:
        """A method getting user by account id.

        Args:
            account_id (int): The account id of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        user_data = await self._repository.get_by_account_id(account_id)

        if not user_data:
            return None

        return UserDTO.from_record(user_data)

    async def get_by_id(self, user_id: int) -> UserDTO | None:
        """A method getting user by account id.

        Args:
            user_id (int): The id of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        if user := await self._repository.get_by_id(user_id):
            return UserDTO.from_record(user)
        return None

    async def update_user(self, account_id: UUID4, data: UserIn) -> UserDTO | None:
        """The method updating user data in the data storage.

        Args:
            account_id (UUID): The id of the user.
            data (UserIn): The details of the updated user info.

        Returns:
            UserDTO | None: The updated user details.
        """

        user_data = await self._repository.update_user(
            account_id=account_id,
            data=data,
        )

        if not user_data:
            return None

        return UserDTO.from_record(user_data)