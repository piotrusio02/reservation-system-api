"""Module containing company repository database implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join
from pydantic import UUID4
from sqlalchemy import and_

from src.core.domain.company import CompanyIn
from src.core.repositories.icompany import ICompanyRepository
from src.db import company_table, account_table, category_table, database

class CompanyRepository(ICompanyRepository):
    """A class implementing the database company repository."""

    async def create_company(self, account_id: UUID4, data: CompanyIn) -> Any | None:
        """The abstract creating new company

        Args:
            account_id (UUID4): The UUID4 of the account.
            data (CompanyIn): The company information

        Returns:
            Any: The newly created company object
        """

        if await self.get_by_account_id(account_id):
            return None

        insert_data = data.model_dump()
        insert_data["account_id"] = account_id

        query = company_table.insert().values(**insert_data)
        await database.execute(query)

        new_company = await self.get_by_account_id(account_id)

        return new_company if new_company else None

    async def get_by_account_id(self, account_id: UUID4) -> Any | None:
        """The abstract getting user by provided account id.

        Args:
            account_id (UUID4): The id of the account.

        Returns:
            Any | None: The company account details
        """

        query = (
            select(company_table, category_table, account_table)
            .select_from(company_table)
            .join(
                category_table,
                company_table.c.category_id == category_table.c.id
            )
            .join(
                account_table,
                company_table.c.account_id == account_table.c.id
            )
            .where(company_table.c.account_id == account_id)
            .order_by(company_table.c.account_id.asc())
        )
        return await database.fetch_one(query)

    async def get_by_id(self, company_id: int) -> Any | None:
        """The abstract getting company by provided id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Any | None: The company account details
        """

        query = (
            select(company_table, category_table, account_table)
            .select_from(company_table)
            .join(
                category_table,
                company_table.c.category_id == category_table.c.id
            )
            .join(
                account_table,
                company_table.c.account_id == account_table.c.id
            )
            .where(company_table.c.id == company_id)
            .order_by(company_table.c.id.asc())
        )

        return await database.fetch_one(query)

    async def get_by_city_and_category(self, city: str, category_id: int) -> Iterable[Any]:
        """The abstract getting all company by city and category from the data storage.

         Returns:
             Iterable[Any]: The collection of the all companies.
         """

        query = (
            select(company_table, category_table, account_table)
            .select_from(company_table)
            .join(
                category_table,
                company_table.c.category_id == category_table.c.id
            )
            .join(
                account_table,
                company_table.c.account_id == account_table.c.id
            )
            .where(and_(company_table.c.category_id == category_id,
                         company_table.c.city == city))
            .order_by(company_table.c.id.asc())
        )

        return await database.fetch_all(query)


    async def update_company(self, account_id: UUID4, data: CompanyIn) -> Any | None:
        """The abstract updating user information.

        Args:
            account_id (UUID4): The id of the account company.
            data (CompanyIn): The new Company information

        Returns:
            Any | None: The updated company.
        """

        if await self.get_by_account_id(account_id=account_id):
            query = (
                company_table.update()
                .where(company_table.c.account_id == account_id)
                .values(**data.model_dump(exclude_none=True))
            )
            await database.execute(query)

            company = await self.get_by_account_id(account_id=account_id)

            return company if company else None

        return None

    async def _get_by_id(self, company_id: int) -> Record | None:
        """A private method getting company from the DB based on its ID.

        Args:
            company_id (int): The ID of the user.

        Returns:
            Any | None: Company record if exists.
        """

        query = (
            select(company_table, category_table, account_table)
            .select_from(company_table)
            .join(
                category_table,
                company_table.c.category_id == category_table.c.id
            )
            .join(
                account_table,
                company_table.c.account_id == account_table.c.id
            )
            .where(company_table.c.id == company_id)
            .order_by(company_table.c.id.asc())
        )

        return await database.fetch_one(query)