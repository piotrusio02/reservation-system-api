"""Module containing employee repository database implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, and_


from src.core.domain.employee import EmployeeIn
from src.core.repositories.iemployee import IEmployeeRepository
from src.db import employee_table, database

class EmployeeRepository(IEmployeeRepository):
    """A class implementing the employee repository."""

    async def create_employee(self, company_id: int, data: EmployeeIn) -> Any | None:
        """The method creating new employee

        Args:
            company_id (int): The id of the company.
            data (EmployeeIn): The attributes of the employee

        Returns:
            Any: The newly created employee object
        """

        insert_data = data.model_dump()
        insert_data["company_id"] = company_id

        query = employee_table.insert().values(**insert_data)
        new_employee_id = await database.execute(query)
        new_employee = await self.get_employee_by_id(company_id=company_id,
                                                     employee_id=new_employee_id)

        return new_employee if new_employee else None

    async def get_employee_by_id(self, company_id: int, employee_id: int) -> Any | None:
        """The method getting an employee from the data storage.

        Args:
            company_id (int): The id of the company.
            employee_id (int): The id of the employee.

        Returns:
            Any | None: The employee data if exists.
        """

        query = (
            employee_table.select()
            .where(and_(employee_table.c.id == employee_id, employee_table.c.company_id == company_id))
            .order_by(employee_table.c.id.asc())
        )
        employee = await database.fetch_one(query)

        return employee if employee else None

    async def get_employees_by_company_id(self, company_id: int) -> Iterable[Any] | None:
        """The method getting all employees by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Any | None: The collection of the all employees for company.
        """

        query = (
            employee_table.select()
            .where(employee_table.c.company_id == company_id)
            .order_by(employee_table.c.first_name.asc())
        )

        return await database.fetch_all(query)

    async def update_employee(self, company_id: int, employee_id: int, data: EmployeeIn) -> Any | None:
        """The method updating employee information.

        Args:
            company_id (int): The id of the company.
            employee_id (int): The id of the employee.
            data (EmployeeIn): The new employee information

        Returns:
            Any | None: The updated employee.
        """

        if await self.get_employee_by_id(company_id=company_id, employee_id=employee_id):
            query = (
                employee_table.update()
                .where(and_(employee_table.c.id == employee_id, employee_table.c.company_id == company_id))
                .values(**data.model_dump(exclude_none=True))
            )
            await database.execute(query)

            employee = await self.get_employee_by_id(company_id=company_id, employee_id=employee_id)

            return employee if employee else None

        return None

    async def delete_employee(self, company_id: int, employee_id: int) -> bool:
        """The method updating removing employee from the data storage.

        Args:
            company_id (int): The id of the company.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """

        if await self.get_employee_by_id(company_id=company_id, employee_id=employee_id):
            query = (
                employee_table.delete()
                .where(and_(employee_table.c.id == employee_id, employee_table.c.company_id == company_id))
            )
            await database.execute(query)

            return True

        return False

    async def is_email_exist(self, email: str) -> bool:
        """A method checking if an employee with email already exist

        Args:
            email (str): The email of the employee.

        Returns:
            bool: Status of the operation.
        """

        query = employee_table \
            .select() \
            .where(employee_table.c.email == email)
        if await database.fetch_one(query):
            return True
        return False