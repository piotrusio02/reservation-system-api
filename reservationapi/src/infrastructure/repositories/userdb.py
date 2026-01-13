"""Module containing user repository database implementation."""

from typing import Any

from asyncpg import Record
from sqlalchemy import select
from pydantic import UUID4

from src.core.domain.user import UserIn
from src.core.repositories.iuser import IUserRepository
from src.db import user_table, account_table, database

class UserRepository(IUserRepository):
    """A class implementing the database user repository."""

    async def create_user(self, account_id: UUID4, data: UserIn) -> Any | None:
        """The abstract creating new user

        Args:
            account_id (UUID4): The UUID4 of the account.
            data (UserIn): account_id, First name, Last name

        Returns:
            Any: The newly created user object
        """

        if await self.get_by_account_id(account_id):
            return None

        insert_data = data.model_dump()
        insert_data["account_id"] = account_id

        query = user_table.insert().values(**insert_data)
        await database.execute(query)

        new_user = await self.get_by_account_id(account_id)

        return new_user if new_user else None

    async def get_by_account_id(self, account_id: UUID4) -> Any | None:
        """The abstract getting user by provided account id.

        Args:
            account_id (UUID4): The id of the account.

        Returns:
            Any | None: The user account details
        """

        query = (
            select(user_table, account_table)
            .select_from(user_table)
            .join(
                account_table,
                user_table.c.account_id == account_table.c.id
            )
            .where(user_table.c.account_id == account_id)
            .order_by(user_table.c.account_id.asc())
        )

        return await database.fetch_one(query)

    async def get_by_id(self, user_id: int) -> Any | None:
        """The abstract getting user by provided id.

        Args:
            user_id (int): The id of the user.

        Returns:
            Any | None: The user account details
        """

        query = (
            select(user_table, account_table)
            .select_from(user_table)
            .join(
                account_table,
                user_table.c.account_id == account_table.c.id
            )
            .where(user_table.c.id == user_id)
            .order_by(user_table.c.id.asc())
        )

        return await database.fetch_one(query)

    async def update_user(self, account_id: UUID4, data: UserIn) -> Any | None:
        """The abstract updating user information.

        Args:
            account_id (UUID4): The id of the account user.
            data (UserIn): The new user information

        Returns:
            Any | None: The updated user.
        """

        if await self.get_by_account_id(account_id=account_id):
            query = (
                user_table.update()
                .where(user_table.c.account_id == account_id)
                .values(**data.model_dump(exclude_none=True))
            )
            await database.execute(query)

            user = await self.get_by_account_id(account_id=account_id)

            return user if user else None

        return None

    async def _get_by_id(self, user_id: int) -> Record | None:
        """A private method getting user from the DB based on its ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Any | None: User record if exists.
        """

        query = (
            select(user_table, account_table)
            .select_from(user_table)
            .join(
                account_table,
                user_table.c.account_id == account_table.c.id
            )
            .where(user_table.c.id == user_id)
            .order_by(user_table.c.id.asc())
        )

        return await database.fetch_one(query)