"""Module containing employee repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from src.core.domain.employee import EmployeeIn

class IEmployeeRepository(ABC):
    """An abstract class representing protocol of employee repository."""

    @abstractmethod
    async def create_employee(self, company_id: int, data: EmployeeIn) -> Any | None:
        """The abstract creating new employee

        Args:
            company_id (int): The id of the company.
            data (EmployeeIn): The attributes of the employee.

        Returns:
            Any: The newly created employee object
        """

    @abstractmethod
    async def get_employee_by_id(self, company_id: int, employee_id: int) -> Any | None:
        """The abstract getting an employee from the data storage.

        Args:
            company_id (int): The id of the company.
            employee_id (int): The id of the employee.

        Returns:
            Any | None: The employee data if exists.
        """

    @abstractmethod
    async def get_employees_by_company_id(self, company_id: int) -> Iterable[Any] | None:
        """The abstract getting all employees by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Any | None: The collection of the all employees for company.
        """

    @abstractmethod
    async def update_employee(self, company_id: int, employee_id: int, data: EmployeeIn) -> Any | None:
        """The abstract updating employee information.

        Args:
            company_id (int): The id of the company.
            employee_id (int): The id of the employee.
            data (EmployeeIn): The new employee information

        Returns:
            Any | None: The updated employee.
        """

    @abstractmethod
    async def delete_employee(self, company_id: int, employee_id: int) -> bool:
        """The abstract updating removing employee from the data storage.

        Args:
            company_id (int): The id of the company.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def is_email_exist(self, email: str) -> bool:
        """A method checking the employee exist by email

        Args:
            email (str): The email of the employee.

        Returns:
            bool: Status of the operation.
        """