"""Module containing company service repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from src.core.domain.company_service import CompanyServiceIn, CompanyServiceUpdateIn


class ICompanyServiceRepository(ABC):
    """An abstract class representing protocol of service repository."""

    @abstractmethod
    async def create_service(self, company_id: int, data: CompanyServiceIn) -> Any | None:
        """The abstract creating new company service

        Args:
            company_id (int): The id of the company.
            data (ServiceIn): The attributes of the service

        Returns:
            Any: The newly created company service object
        """

    @abstractmethod
    async def get_service_by_id(self, service_id: int) -> Any | None:
        """The abstract getting a company service from the data storage.

        Args:
            service_id (int): The id of the service.

        Returns:
            Any | None: The service data if exists.
        """

    @abstractmethod
    async def get_services_by_company_id(self, company_id: int) -> Iterable[Any] | None:
        """The abstract getting all company services by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Any | None: The collection of the all services for company.
        """

    @abstractmethod
    async def get_services_by_company_id_and_subcategory_id(self, company_id: int, subcategory_id: int) -> Iterable[Any] | None:
        """The abstract getting all company services by provided company id.

        Args:
            company_id (int): The id of the company.
            subcategory_id (int): The id of the company subcategory

        Returns:
            Any | None: The collection of the all services for company and subcategory.
        """

    @abstractmethod
    async def update_service(self, company_id: int, service_id: int, data: CompanyServiceUpdateIn) -> Any | None:
        """The abstract updating company service information.

        Args:
            company_id (int): The id of the company.
            service_id (int): The id of the service.
            data (ServiceIn): The new service information

        Returns:
            Any | None: The updated service.
        """

    @abstractmethod
    async def delete_service(self, company_id: int, service_id: int) -> bool:
        """The abstract updating removing employee from the data storage.

        Args:
            company_id (int): The id of the company.
            service_id (int): The id of the service.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_employees_by_service_id_public(self, service_id: int) -> Iterable[Any] | None:
        """The method getting all employees for service by provided service id.

        Args:
            service_id (int): The id of the service.

        Returns:
            Any | None: The collection of the all  employees public for service.
        """

    @abstractmethod
    async def get_employees_by_service_id(self, company_id: int, service_id: int) -> Iterable[Any] | None:
        """The abstract getting all employees for service by provided service id.

        Args:
            company_id (int): The id of the company.
            service_id (int): The id of the service.

        Returns:
            Any | None: The collection of the all  employees for service.
        """

    @abstractmethod
    async def add_employee_to_service(self, service_id: int, employee_id: int) -> bool:
        """The abstract adding new employee to service

        Args:
            service_id (int): The id of the service.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def remove_employee_from_service(self, service_id: int, employee_id: int) -> bool:
        """The method updating removing employee from service

        Args:
            service_id (int): The id of the service.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def update_is_active(self, service_id: int, is_active: bool) -> None:
        """The private method updating active status in service

        Args:
            service_id (int): The id of the service.
            is_active (bool): Status from service.
        """