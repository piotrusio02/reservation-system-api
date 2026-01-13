"""Module containing company subcategory repository database implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, and_


from src.core.domain.company_subcategory import SubcategoryIn
from src.core.repositories.icompany_subcategory import ICompanySubcategoryRepository
from src.db import company_subcategory_table, database

class CompanySubcategoryRepository(ICompanySubcategoryRepository):
    """A class implementing the company subcategory repository."""

    async def create_subcategory(self, company_id: int, data: SubcategoryIn) -> Any | None:
        """The method creating new company subcategory

        Args:
            company_id (int): The id of the company.
            data (SubcategoryIn): The attributes of the new subcategory

        Returns:
            Any: The newly created subcategory object
        """

        insert_data = data.model_dump()
        insert_data["company_id"] = company_id

        query = company_subcategory_table.insert().values(**insert_data)
        new_subcategory_id = await database.execute(query)
        new_subcategory = await self.get_subcategory_by_id(company_id=company_id,
                                                     subcategory_id=new_subcategory_id)

        return new_subcategory if new_subcategory else None

    async def get_subcategories_by_company_id(self, company_id: int) -> Iterable[Any] | None:
        """The method getting all subcategories by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Any | None: The collection of the all subcategories for company.
        """

        query = (
            company_subcategory_table.select()
            .where(company_subcategory_table.c.company_id == company_id)
            .order_by(company_subcategory_table.c.name.asc())
        )

        return await database.fetch_all(query)

    async def update_subcategory(self, company_id: int, subcategory_id: int, data: SubcategoryIn) -> Any | None:
        """The method updating subcategory information.

        Args:
            company_id (int): The id of the company.
            subcategory_id (int): The id of the subcategory.
            data (SubcategoryIn): The new subcategory information

        Returns:
            Any | None: The updated subcategory.
        """

        if await self.get_subcategory_by_id(company_id=company_id, subcategory_id=subcategory_id):
            query = (
                company_subcategory_table.update()
                .where(and_(company_subcategory_table.c.id == subcategory_id,
                            company_subcategory_table.c.company_id == company_id))
                .values(**data.model_dump())
            )
            await database.execute(query)

            subcategory = await self.get_subcategory_by_id(company_id=company_id, subcategory_id=subcategory_id)

            return subcategory if subcategory else None

        return None

    async def delete_subcategory(self, company_id: int, subcategory_id: int) -> bool:
        """The method updating removing subcategory from the data storage.

        Args:
            company_id (int): The id of the company.
            subcategory_id (int): The subcategory id.

        Returns:
            bool: Success of the operation.
        """

        if await self.get_subcategory_by_id(company_id=company_id, subcategory_id=subcategory_id):
            query = (
                company_subcategory_table.delete()
                .where(and_(company_subcategory_table.c.id == subcategory_id,
                            company_subcategory_table.c.company_id == company_id))
            )
            await database.execute(query)

            return True

        return False


    async def get_subcategory_by_id(self, company_id: int, subcategory_id: int) -> Any | None:
        """The method getting an employee from the data storage.

        Args:`
            company_id (int): The id of the company.
            subcategory_id (int): The id of the subcategory.

        Returns:
            Any | None: The subcategory data if exists.
        """

        query = (
            company_subcategory_table.select()
            .where(and_(company_subcategory_table.c.id == subcategory_id,
                        company_subcategory_table.c.company_id == company_id))
            .order_by(company_subcategory_table.c.id.asc())
        )
        subcategory = await database.fetch_one(query)

        return subcategory if subcategory else None