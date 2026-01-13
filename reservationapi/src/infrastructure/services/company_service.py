"""A module containing "company service" service."""

from typing import Iterable

from pydantic import UUID4

from src.core.domain.company_service import CompanyServiceIn, CompanyServiceUpdateIn
from src.core.repositories.icompany_service import ICompanyServiceRepository
from src.core.repositories.icompany import ICompanyRepository
from src.core.repositories.icompany_subcategory import ICompanySubcategoryRepository
from src.core.repositories.iemployee import IEmployeeRepository
from src.infrastructure.dto.company_servicedto import ServiceDTO, ServiceListDTO, ServicePublicDTO
from src.infrastructure.dto.employeedto import EmployeeDTO, EmployeePublicDTO
from src.infrastructure.services.icompany_service import ICompanyServiceService

class CompanyServiceService(ICompanyServiceService):
    """A class implementing the "company service" service."""

    _s_repository: ICompanyServiceRepository
    _c_repository: ICompanyRepository
    _sc_repository: ICompanySubcategoryRepository
    _e_repository: IEmployeeRepository


    def __init__(self, s_repository: ICompanyServiceRepository, c_repository: ICompanyRepository,
                 sc_repository: ICompanySubcategoryRepository, e_repository: IEmployeeRepository) -> None:
        """The initializer of the "company service" service.

        Args:
            s_repository (ICompanyServiceRepository): The reference to the company service repository.
            c_repository (ICompanyRepository): The reference to the company repository.
            sc_repository (ICompanySubcategoryRepository): The reference to the company subcategory repository.
            e_repository (IEmployeeRepository): The reference to the employee repository.
        """

        self._s_repository = s_repository
        self._c_repository = c_repository
        self._sc_repository = sc_repository
        self._e_repository = e_repository

    async def create_service(self, account_id: UUID4, data: CompanyServiceIn) -> ServiceDTO | None:
        """The method creating new company service

        Args:
            account_id (UUID4): The account id of the company.
            data (ServiceIn): The attributes of the service

        Returns:
            ServiceDTO | None: The company service DTO model.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        if not await self._sc_repository.get_subcategory_by_id(company_id=company_id, subcategory_id=data.subcategory_id):
            return None

        if data.duration_minutes % 15 != 0:
            return None

        service_data = await self._s_repository.create_service(company_id=company_id, data=data)

        if not service_data:
            return None

        return ServiceDTO.from_record(service_data)

    async def get_service_by_id(self, service_id: int) -> ServiceDTO | None:
        """The method getting a company service from the data storage.

        Args:
            service_id (int): The id of the service.

        Returns:
            ServiceDTO | None: The company service DTO model.
        """

        service_data = await self._s_repository.get_service_by_id(service_id=service_id)

        if not service_data:
            return None

        return ServiceDTO.from_record(service_data)

    async def get_service_by_id_public(self, service_id: int) -> ServicePublicDTO | None:
        """The method getting a company service from the data storage.

        Args:
            service_id (int): The id of the service.

        Returns:
            ServicePublicDTO | None: The company service public DTO model.
        """

        service_data = await self._s_repository.get_service_by_id(service_id=service_id)

        if not service_data:
            return None

        return ServicePublicDTO.from_record(service_data)

    async def get_services(self, account_id: UUID4) -> Iterable[ServiceListDTO] | None:
        """The method getting all services from the data storage.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            Iterable[ServiceListDTO]: The collection of the all services.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        services = await self._s_repository.get_services_by_company_id(company_id=company_id)

        return [ServiceListDTO.from_record(service) for service in services]

    async def get_services_by_company_id(self, company_id: int) -> Iterable[ServiceListDTO] | None:
        """The method getting all company services by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[ServiceListDTO]: The collection of the all company services.
        """

        services = await self._s_repository.get_services_by_company_id(company_id=company_id)

        return [ServiceListDTO.from_record(service) for service in services]

    async def get_services_by_company_id_and_subcategory_id(self, company_id: int, subcategory_id: int) -> Iterable[ServiceListDTO] | None:
        """The method getting all company services by provided company id.

        Args:
            company_id (int): The id of the company.
            subcategory_id (int): The id of the company subcategory

        Returns:
            Iterable[ServiceListDTO]: The collection of the all company services.
        """

        services = await self._s_repository.get_services_by_company_id_and_subcategory_id(company_id=company_id, subcategory_id=subcategory_id)

        return [ServiceListDTO.from_record(service) for service in services]

    async def update_service(self, account_id: UUID4, service_id: int, data: CompanyServiceUpdateIn) -> ServiceDTO | None:
        """The method updating company service information.

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.
            data (ServiceIn): The new service information

        Returns:
            ServiceDTO | None: The updated employee details.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        if data.subcategory_id:

            subcategory = await self._sc_repository.get_subcategory_by_id(company_id=company_id,
                                                                   subcategory_id=data.subcategory_id)

            if not subcategory:
                return None

        if data.duration_minutes is not None and data.duration_minutes % 15 != 0:
            return None

        service_data = await self._s_repository.update_service(company_id=company_id, service_id=service_id, data=data)

        if not service_data:
            return None

        return ServiceDTO.from_record(service_data)

    async def delete_service(self, account_id: UUID4, service_id: int) -> bool:
        """The method updating removing employee from the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.

        Returns:
            bool: Success of the operation.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return False

        return await self._s_repository.delete_service(company_id=company_id, service_id=service_id)

    async def get_designed_employees_public(self, service_id: int) -> Iterable[EmployeePublicDTO] | None:
        """The method getting all employees for service by provided service id.

        Args:
            service_id (int): The id of the service.

        Returns:
            Iterable[EmployeePublicDTO]: The collection of the all employees from service.
        """

        employees = await self._s_repository.get_employees_by_service_id_public(service_id=service_id)

        return [EmployeePublicDTO(**dict(employee)) for employee in employees]

    async def get_designed_employees(self, account_id: UUID4,  service_id: int) -> Iterable[EmployeeDTO] | None:
        """The method getting all employees for service by provided service id.

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.

        Returns:
            Iterable[EmployeePublicDTO]: The collection of the all employees from service.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        employees = await self._s_repository.get_employees_by_service_id(company_id=company_id, service_id=service_id)

        return [EmployeeDTO(**dict(employee)) for employee in employees]

    async def add_employee_to_service(self, account_id: UUID4, service_id: int, employee_id: int) -> bool:
        """The method adding new employee to service

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return False

        service = await self._s_repository.get_service_by_id(service_id=service_id)

        if not service or service["company_id"] != company_id:
            return False

        if not await self._e_repository.get_employee_by_id(company_id=company_id, employee_id=employee_id):
            return False

        active_employee = await self._s_repository.add_employee_to_service(
            service_id=service_id,
            employee_id=employee_id
        )

        if active_employee:
            await self._s_repository.update_is_active(service_id=service_id, is_active=True)

        return active_employee

    async def remove_employee_from_service(self, account_id: UUID4, service_id: int, employee_id: int) -> bool:
        """The method updating removing employee from service

        Args:
            account_id (UUID4): The account id of the company.
            service_id (int): The id of the service.
            employee_id (int): The id of the employee.

        Returns:
            bool: Success of the operation.
        """
        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return False

        service = await self._s_repository.get_service_by_id(service_id=service_id)

        if not service or service["company_id"] != company_id:
            return False

        if not await self._e_repository.get_employee_by_id(company_id=company_id, employee_id=employee_id):
            return False

        if await self._s_repository.remove_employee_from_service(service_id=service_id, employee_id=employee_id):
            employees = await self._s_repository.get_employees_by_service_id_public(service_id=service_id)
            is_active = len(list(employees)) > 0
            await self._s_repository.update_is_active(service_id=service_id, is_active=is_active)

            return True
        return False


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
