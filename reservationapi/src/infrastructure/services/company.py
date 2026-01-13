"""A module containing company service."""

from typing import Iterable

from pydantic import UUID4

from src.core.domain.company import CompanyIn
from src.core.repositories.icompany import ICompanyRepository
from src.core.repositories.icategory import ICategoryRepository
from src.infrastructure.dto.companydto import CompanyDTO, CompanyPublicDTO, CompanyListDTO
from src.infrastructure.services.icompany import ICompanyService

class CompanyService(ICompanyService):
    """A class implementing the company service."""

    _repository: ICompanyRepository
    _c_repository: ICategoryRepository
    def __init__(self, repository: ICompanyRepository, c_repository: ICategoryRepository,) -> None:
        """The initializer of the company service.

        Args:
            repository (ICompanyRepository): The reference to the company repository.
            c_repository (ICategoryRepository): The reference to the category repository.
        """

        self._repository = repository
        self._c_repository = c_repository

    async def create_company(self, account_id: UUID4, company: CompanyIn) -> CompanyDTO | None:
        """A method create a new company.

        Args:
            account_id (UUID4): The account id of the company.
            company (CompanyIn): The company input data.

        Returns:
            CompanyDTO | None: The company DTO model.
        """

        if not await self._c_repository.get_category_by_id(category_id=company.category_id):
            return None

        company_data = await self._repository.create_company(account_id, company)

        if not company_data:
            return None

        return CompanyDTO.from_record(company_data)

    async def get_by_account_id(self, account_id: UUID4) -> CompanyDTO | None:
        """A method getting company by account id.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            CompanyDTO | None: The company data, if found.
        """

        company_data = await self._repository.get_by_account_id(account_id)

        if not company_data:
            return None

        return CompanyDTO.from_record(company_data)

    async def get_by_id(self, company_id: int) -> CompanyPublicDTO | None:
        """A method getting company by account id.

        Args:
            company_id (int): The id of the company.

        Returns:
            CompanyPublicDTO | None: The company data, if found.
        """

        company_data = await self._repository.get_by_id(company_id)

        if not company_data:
            return None

        return CompanyPublicDTO.from_record(company_data)

    async def get_by_city_and_category(self, city: str, category_id: int) -> Iterable[CompanyListDTO]:
        """The abstract getting all company by city and category from the data storage.

        Args:
            city (str): City for filtering.
            category_id (int): The id of the category.

        Returns:
            Iterable[CompanyListDTO]: The collection of the all company by city and category.
        """

        companies = await self._repository.get_by_city_and_category(city=city, category_id=category_id)

        return [CompanyListDTO.from_record(company) for company in companies]

    async def update_company(self, account_id: UUID4, data: CompanyIn) -> CompanyDTO | None:
        """The method updating company data in the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            data (CompanyIn): The details of the updated company info.

        Returns:
            CompanyDTO | None: The updated company details.
        """

        company_data = await self._repository.update_company(
            account_id=account_id,
            data=data,
        )

        if not company_data:
            return None

        return CompanyDTO.from_record(company_data)