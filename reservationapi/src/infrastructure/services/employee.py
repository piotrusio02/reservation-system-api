"""A module containing employee service."""

from typing import Iterable

from pydantic import UUID4

from src.core.domain.employee import EmployeeIn
from src.core.repositories.iemployee import IEmployeeRepository
from src.core.repositories.icompany import ICompanyRepository
from src.infrastructure.dto.employeedto import EmployeeDTO, EmployeePublicDTO
from src.infrastructure.services.iemployee import IEmployeeService

class EmployeeService(IEmployeeService):
    """A class implementing the employee service."""

    _e_repository: IEmployeeRepository
    _c_repository: ICompanyRepository


    def __init__(self, e_repository: IEmployeeRepository, c_repository: ICompanyRepository) -> None:
        """The initializer of the employee service.

        Args:
            e_repository (IEmployeeRepository): The reference to the employee repository.
            c_repository (ICompanyRepository): The reference to the company repository.
        """

        self._e_repository = e_repository
        self._c_repository = c_repository

    async def create_employee(self, account_id: UUID4, data: EmployeeIn) -> EmployeeDTO | None:
        """A method create a new employee.

        Args:
            account_id (UUID4): The account id of the company.
            data (EmployeeIn): The employee input data.

        Returns:
            EmployeeDTO | None: The employee DTO model.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        if await self._is_email_exist(data.email):
            return None

        employee_data = await self._e_repository.create_employee(company_id=company_id, data=data)

        if not employee_data:
            return None

        return EmployeeDTO(**dict(employee_data))

    async def get_employee_by_id(self, account_id: UUID4, employee_id: int) -> EmployeeDTO | None:
        """The method getting employee from the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            employee_id (int): The id of the employee.

        Returns:
            EmployeeDTO | None: The employee data, if found.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        employee_data = await self._e_repository.get_employee_by_id(company_id=company_id, employee_id=employee_id)

        if not employee_data:
            return None

        return EmployeeDTO(**dict(employee_data))

    async def get_employees(self, account_id: UUID4) -> Iterable[EmployeeDTO] | None:
        """The method getting all employees from the data storage.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            Iterable[EmployeeDTO]: The collection of the all employee.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        employees = await self._e_repository.get_employees_by_company_id(company_id=company_id)

        return [EmployeeDTO(**dict(employee)) for employee in employees]

    async def get_employees_by_company_id(self, company_id: int) -> Iterable[EmployeePublicDTO]:
        """The method getting all employees from the data storage.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[EmployeePublicDTO]: The collection of the all employee.
        """

        employees = await self._e_repository.get_employees_by_company_id(company_id=company_id)

        return [EmployeePublicDTO(**dict(employee)) for employee in employees]

    async def update_employee(self, account_id: UUID4, employee_id: int, data: EmployeeIn) -> EmployeeDTO | None:
        """The method updating employee data in the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            employee_id (int): The id of the employee.
            data (EmployeeIn): The details of the updated employee.

        Returns:
            EmployeeDTO | None: The updated employee details.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        employee_data = await self._e_repository.update_employee(company_id=company_id, employee_id=employee_id, data=data)

        if not employee_data:
            return None

        return EmployeeDTO(**dict(employee_data))

    async def delete_employee(self, account_id: UUID4, employee_id: int) -> bool:
        """The method updating removing employee from the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return False

        return await self._e_repository.delete_employee(company_id=company_id, employee_id=employee_id)



    async def _get_company_id(self, account_id: UUID4) -> int | None:
        """A private method translating account ID to company ID.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            int | None: The company ID
        """

        company = await self._c_repository.get_by_account_id(account_id)

        if not company:
            return None

        return company["id"]

    async def _is_email_exist(self, email: str) -> bool:
        """A private method checking if an employee with email already exist

        Args:
            email (str): The email of the employee.

        Returns:
            bool: Status of the operation.
        """

        return await self._e_repository.is_email_exist(email)