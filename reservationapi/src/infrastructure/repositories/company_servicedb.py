"""Module containing company service repository database implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, and_

from src.core.domain.company_service import CompanyServiceIn, CompanyServiceUpdateIn
from src.core.repositories.icompany_service import ICompanyServiceRepository
from src.db import company_service_table, service_employee_table, company_table, account_table, category_table, company_subcategory_table, employee_table, database

class CompanyServiceRepository(ICompanyServiceRepository):
    """A class implementing the company service repository."""

    async def create_service(self, company_id: int, data: CompanyServiceIn) -> Any | None:
        """The method creating new company service

        Args:
            company_id (int): The id of the company.
            data (CompanyServiceIn): The attributes of the service

        Returns:
            Any: The newly created company service object
        """

        insert_data = data.model_dump(exclude={"designated_employees"})
        insert_data["company_id"] = company_id
        insert_data["is_active"] = False

        query = company_service_table.insert().values(**insert_data)
        new_service_id = await database.execute(query)
        new_service =await self.get_service_by_id(new_service_id)

        if not new_service:
            return None

        return new_service if new_service else None


    async def get_service_by_id(self, service_id: int) -> Any | None:
        """The method getting a company service from the data storage.

        Args:
            service_id (int): The id of the service.

        Returns:
            Any | None: The service data if exists.
        """

        query = (
            select(company_service_table, company_subcategory_table, company_table, category_table, account_table)
            .select_from(company_service_table)
            .join(
                company_subcategory_table,
                company_service_table.c.subcategory_id == company_subcategory_table.c.id
            )
            .join(
                company_table,
                company_service_table.c.company_id == company_table.c.id
            )
            .join(
                category_table,
                company_table.c.category_id == category_table.c.id
            )
            .join(
                account_table,
                company_table.c.account_id == account_table.c.id
            )

            .where(company_service_table.c.id == service_id)
            .order_by(company_service_table.c.id.asc())
        )

        return await database.fetch_one(query)

    async def get_services_by_company_id(self, company_id: int) -> Iterable[Any] | None:
        """The method getting all company services by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Any | None: The collection of the all services for company.
        """

        query = (
            select(company_service_table)
            .where(company_service_table.c.company_id == company_id)
            .order_by(company_service_table.c.subcategory_id.asc())
        )

        return await database.fetch_all(query)

    async def get_services_by_company_id_and_subcategory_id(self, company_id: int, subcategory_id: int) -> Iterable[Any] | None:
        """The method getting all company services by provided company id.

        Args:
            company_id (int): The id of the company.
            subcategory_id (int): The id of the company subcategory

        Returns:
            Any | None: The collection of the all services for company and subcategory.
        """

        query = (
            select(company_service_table)
            .where(and_(company_service_table.c.company_id == company_id,
                        company_service_table.c.subcategory_id == subcategory_id))
            .order_by(company_service_table.c.id.asc())
        )

        return await database.fetch_all(query)

    async def update_service(self, company_id: int, service_id: int, data: CompanyServiceUpdateIn) -> Any | None:
        """The method updating company service information.

        Args:
            company_id (int): The id of the company.
            service_id (int): The id of the service.
            data (ServiceIn): The new service information

        Returns:
            Any | None: The updated service.
        """
        if await self.get_service_by_id(service_id=service_id):
            query = (
                company_service_table.update()
                .where(and_(company_service_table.c.company_id == company_id,
                            company_service_table.c.id == service_id))
                .values(**data.model_dump(exclude_none=True))
            )
            await database.execute(query)

            service = await self.get_service_by_id(service_id=service_id)

            return service if service else None

        return None


    async def delete_service(self, company_id: int, service_id: int) -> bool:
        """The method updating removing employee from the data storage.

        Args:
            company_id (int): The id of the company.
            service_id (int): The id of the service.

        Returns:
            bool: Success of the operation.
        """
        if await self.get_service_by_id(service_id=service_id):
            query = (
                company_service_table.delete()
                .where(and_(company_service_table.c.id == service_id,
                            company_service_table.c.company_id == company_id))
            )
            await database.execute(query)

            return True

        return False


    async def get_employees_by_service_id_public(self, service_id: int) -> Iterable[Any] | None:
        """The method getting all employees for service by provided service id.

        Args:
            service_id (int): The id of the service.

        Returns:
            Any | None: The collection of the all  employees public for service.
        """
        query = (
            select(
                employee_table.c.id,
                employee_table.c.first_name,
                employee_table.c.last_name,
            )
            .select_from(service_employee_table)
            .join(
                employee_table,
                service_employee_table.c.employee_id == employee_table.c.id
            )
            .where(service_employee_table.c.service_id == service_id)
            .order_by(service_employee_table.c.employee_id.asc())
        )

        return await database.fetch_all(query)

    async def get_employees_by_service_id(self, company_id: int, service_id: int) -> Iterable[Any] | None:
        """The method getting all employees for service by provided service id.

        Args:
            company_id (int): The id of the company.
            service_id (int): The id of the service.

        Returns:
            Any | None: The collection of the all  employees for service.
        """
        query = (
            select(
                employee_table.c.id,
                employee_table.c.first_name,
                employee_table.c.last_name,
                employee_table.c.email,
                employee_table.c.phone_number
            )
            .select_from(service_employee_table)
            .join(
                employee_table,
                service_employee_table.c.employee_id == employee_table.c.id
            )
            .join(
                company_service_table,
                service_employee_table.c.service_id == company_service_table.c.id
            )
            .where(and_(service_employee_table.c.service_id == service_id,
                        company_service_table.c.company_id == company_id))
            .order_by(service_employee_table.c.employee_id.asc())
        )

        return await database.fetch_all(query)

    async def add_employee_to_service(self, service_id: int, employee_id: int) -> bool:
        """The method adding new employee to service

        Args:
            service_id (int): The id of the service.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """

        query = service_employee_table.insert().values(
            service_id=service_id,
            employee_id=employee_id
        )
        await database.execute(query)
        return True

    async def remove_employee_from_service(self, service_id: int, employee_id: int) -> bool:
        """The method updating removing employee from service

        Args:
            service_id (int): The id of the service.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """

        query = (
            service_employee_table.delete()
            .where(and_(service_employee_table.c.service_id == service_id,
                        service_employee_table.c.employee_id == employee_id))
        )
        await database.execute(query)
        return True

    async def update_is_active(self, service_id: int, is_active: bool) -> None:
        """The private method updating active status in service

        Args:
            service_id (int): The id of the service.
            is_active (bool): Status from service.
        """

        query = (
            company_service_table.update()
            .where(company_service_table.c.id == service_id)
            .values(is_active=is_active)
        )
        await database.execute(query)

