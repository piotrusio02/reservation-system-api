"""A module containing "company service" service."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.company_service import CompanyServiceIn, CompanyServiceUpdateIn
from src.infrastructure.dto.company_servicedto import ServiceDTO, ServiceListDTO, ServicePublicDTO
from src.infrastructure.dto.employeedto import EmployeeDTO, EmployeePublicDTO


class ICompanyServiceService(ABC):
    """An abstract class for "company service" service."""

    @abstractmethod
    async def create_service(self, account_id: UUID4, data: CompanyServiceIn) -> ServiceDTO | None:
        """The abstract creating new company service

        Args:
            account_id (UUID4): The account id of the company.
            data (ServiceIn): The attributes of the service

        Returns:
            ServiceDTO | None: The company service DTO model.
        """

    @abstractmethod
    async def get_service_by_id(self, service_id: int) -> ServiceDTO | None:
        """The abstract getting a company service from the data storage.

        Args:
            service_id (int): The id of the service.

        Returns:
            ServiceDTO | None: The company service DTO model.
        """

    async def get_service_by_id_public(self, service_id: int) -> ServicePublicDTO | None:
        """The method getting a company service from the data storage.

        Args:
            service_id (int): The id of the service.

        Returns:
            ServicePublicDTO | None: The company service public DTO model.
        """

    @abstractmethod
    async def get_services(self, account_id: UUID4) -> Iterable[ServiceListDTO] | None:
        """The method getting all services from the data storage.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            Iterable[ServiceListDTO]: The collection of the all services.
        """

    @abstractmethod
    async def get_services_by_company_id(self, company_id: int) -> Iterable[ServiceListDTO] | None:
        """The abstract getting all company services by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[ServiceListDTO]: The collection of the all company services.
        """

    @abstractmethod
    async def get_services_by_company_id_and_subcategory_id(self, company_id: int, subcategory_id: int) -> Iterable[ServiceListDTO] | None:
        """The abstract getting all company services by provided company id.

        Args:
            company_id (int): The id of the company.
            subcategory_id (int): The id of the company subcategory

        Returns:
            Iterable[ServiceListDTO]: The collection of the all company services.
        """

    @abstractmethod
    async def update_service(self, account_id: UUID4, service_id: int, data: CompanyServiceUpdateIn) -> ServiceDTO | None:
        """The abstract updating company service information.

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.
            data (ServiceIn): The new service information

        Returns:
            ServiceDTO | None: The updated employee details.
        """

    @abstractmethod
    async def delete_service(self, account_id: UUID4, service_id: int) -> bool:
        """The abstract updating removing employee from the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_designed_employees_public(self, service_id: int) -> Iterable[EmployeePublicDTO] | None:
        """The abstract getting all employees for service by provided service id.

        Args:
            service_id (int): The id of the service.

        Returns:
            Iterable[EmployeePublicDTO]: The collection of the all employees from service.
        """

    @abstractmethod
    async def get_designed_employees(self, account_id: UUID4,  service_id: int) -> Iterable[EmployeeDTO] | None:
        """The abstract getting all employees for service by provided service id.

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.

        Returns:
            Iterable[EmployeePublicDTO]: The collection of the all employees from service.
        """

    @abstractmethod
    async def add_employee_to_service(self, account_id: UUID4, service_id: int, employee_id: int) -> bool:
        """The abstract adding new employee to service

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def remove_employee_from_service(self, account_id: UUID4, service_id: int, employee_id: int) -> bool:
        """The method updating removing employee from service

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """