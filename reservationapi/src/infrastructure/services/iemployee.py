"""A module containing employee service."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.employee import EmployeeIn
from src.infrastructure.dto.employeedto import EmployeeDTO, EmployeePublicDTO


class IEmployeeService(ABC):
    """An abstract class for employee service."""

    @abstractmethod
    async def create_employee(self, account_id: UUID4, data: EmployeeIn) -> EmployeeDTO | None:
        """A method create a new employee.

        Args:
            account_id (UUID4): The account id of the company.
            data (EmployeeIn): The employee input data.

        Returns:
            EmployeeDTO | None: The employee DTO model.
        """

    @abstractmethod
    async def get_employee_by_id(self, account_id: UUID4, employee_id: int) -> EmployeeDTO | None:
        """The abstract getting employee from the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            employee_id (int): The id of the employee.

        Returns:
            EmployeeDTO | None: The employee data, if found.
        """

    @abstractmethod
    async def get_employees(self, account_id: UUID4) -> Iterable[EmployeeDTO] | None:
        """The abstract getting all employees from the data storage.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            Iterable[EmployeeDTO]: The collection of the all employee.
        """

    @abstractmethod
    async def get_employees_by_company_id(self, company_id: int) -> Iterable[EmployeePublicDTO] | None:
        """The abstract getting all employees from the data storage.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[EmployeePublicDTO]: The collection of the all employees.
        """

    @abstractmethod
    async def update_employee(self, account_id: UUID4, employee_id: int, data: EmployeeIn) -> EmployeeDTO | None:
        """The method updating employee data in the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            employee_id (int): The id of the employee.
            data (EmployeeIn): The details of the updated employee.

        Returns:
            EmployeeDTO | None: The updated employee details.
        """

    @abstractmethod
    async def delete_employee(self, account_id: UUID4, employee_id: int) -> bool:
        """The method updating removing employee from the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """