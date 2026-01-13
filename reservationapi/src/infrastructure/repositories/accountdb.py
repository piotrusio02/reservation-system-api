"""A repository for account entity."""

from typing import Any
from datetime import datetime

import sqlalchemy
from asyncpg import Record
from pydantic import UUID4

from src.infrastructure.utils.password import hash_password, verify_password
from src.core.domain.account import Account, AccountIn
from src.core.repositories.iaccount import IAccountRepository
from src.db import database, account_table

class AccountRepository(IAccountRepository):
    """An implementation of repository class for account."""

    async def register_account(self, account: AccountIn) -> Any | None:
        """A method registering new account.

        Args:
            account (AccountIn): The user input data.

        Returns:
            Any | None: The new user object.
        """

        if await self.get_by_email(account.email):
            return None

        account.password = hash_password(account.password)

        insert_data = {
            "email": account.email,
            "phone_number": account.phone_number,
            "password": account.password,
            "role": account.role.value,
            "registration_date": datetime.now()
        }


        query = account_table.insert().values(**insert_data)
        new_account_uuid = await database.execute(query)

        return await self.get_account_by_uuid(new_account_uuid)



    async def get_account_by_uuid(self, uuid: UUID4) -> Any | None:
        """A method getting account by UUID.

        Args:
            uuid (UUID4): UUID of the account.

        Returns:
            Any | None: The account object if exists.
        """

        query = account_table \
            .select() \
            .where(account_table.c.id == uuid)
        account = await database.fetch_one(query)

        return account

    async def get_by_email(self, email: str) -> Any | None:
        """A method getting account by email.

        Args:
            email (str): The email of the account.

        Returns:
            Any | None: The account object if exists.
        """

        query = account_table \
            .select() \
            .where(account_table.c.email == email)
        account = await database.fetch_one(query)

        return account

    async def update_password(self, account_id: UUID4, new_password: str) -> Any | None:
        """A method updating password for account.

        Args:
            account_id (UUID4): UUID of the account.
            new_password (str): new password

        Returns:
            Any | None: The account object if exists.
        """

        if await self._get_by_uuid(account_id):

            new_password = hash_password(new_password)

            query = (
                account_table.update()
                    .where(account_table.c.id == account_id)
                    .values(password = new_password)
            )
            await database.execute(query)

            return await self.get_account_by_uuid(account_id)


        return None


    async def _get_by_uuid(self, account_id: UUID4) -> Record | None:
        """A private method getting account from the DB based on its ID.

        Args:
            account_id (UUID4): The ID of the account.

        Returns:
            Any | None: Account record if exists.
        """
        query = (
            account_table.select()
            .where(account_table.c.id == account_id)
            .order_by(account_table.c.id.asc())
        )
        return await database.fetch_one(query)