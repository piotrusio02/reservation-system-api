"""A module containing company subcategory service."""

from typing import Iterable

from pydantic import UUID4

from src.core.domain.company_subcategory import SubcategoryIn
from src.core.repositories.icompany_subcategory import ICompanySubcategoryRepository
from src.core.repositories.icompany import ICompanyRepository
from src.infrastructure.dto.company_subcategorydto import SubcategoryDTO
from src.infrastructure.services.icompany_subcategory import ICompanySubcategoryService

class CompanySubcategoryService(ICompanySubcategoryService):
    """A class implementing the company subcategory service."""

    _s_repository: ICompanySubcategoryRepository
    _c_repository: ICompanyRepository


    def __init__(self, s_repository: ICompanySubcategoryRepository, c_repository: ICompanyRepository) -> None:
        """The initializer of the company subcategory service.

        Args:
            s_repository (ICompanySubcategoryRepository): The reference to the company subcategory repository.
            c_repository (ICompanyRepository): The reference to the company repository.
        """

        self._s_repository = s_repository
        self._c_repository = c_repository

    async def create_subcategory(self, account_id: UUID4, data: SubcategoryIn) -> SubcategoryDTO | None:
        """A method create a new subcategory.

        Args:
            account_id (UUID4): The account id of the company.
            data (SubcategoryIn): The subcategory input data.

        Returns:
            SubcategoryDTO | None: The subcategory DTO model.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        subcategory_data = await self._s_repository.create_subcategory(company_id=company_id, data=data)

        if not subcategory_data:
            return None

        return SubcategoryDTO(**dict(subcategory_data))

    async def get_subcategories(self, account_id: UUID4) -> Iterable[SubcategoryDTO]:
        """The abstract getting all subcategories for company from the data storage.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            Iterable[SubcategoryDTO]: The collection of the all subcategories for company.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return []

        subcategories = await self._s_repository.get_subcategories_by_company_id(company_id=company_id)

        return [SubcategoryDTO(**dict(subcategory)) for subcategory in subcategories]

    async def get_subcategories_by_company_id(self, company_id: int) -> Iterable[SubcategoryDTO]:
        """The abstract getting all subcategories for company from the data storage.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[SubcategoryDTO]: The collection of the all subcategories for company.
        """

        subcategories = await self._s_repository.get_subcategories_by_company_id(company_id=company_id)

        return [SubcategoryDTO(**dict(subcategory)) for subcategory in subcategories]

    async def update_subcategory(self, account_id: UUID4, subcategory_id: int, data: SubcategoryIn) -> SubcategoryDTO | None:
        """The method updating subcategory data in the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            subcategory_id (int): The id of the subcategory.
            data (SubcategoryIn): The details of the updated subcategory.

        Returns:
            SubcategoryDTO | None: The subcategory DTO model.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        subcategory_data = await self._s_repository.update_subcategory(company_id=company_id,
                                                                    subcategory_id=subcategory_id, data=data)

        if not subcategory_data:
            return None

        return SubcategoryDTO(**dict(subcategory_data))

    async def delete_subcategory(self, account_id: UUID4, subcategory_id: int) -> bool:
        """The method updating removing subcategory from the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            subcategory_id (int): The id of the subcategory.

        Returns:
            bool: Success of the operation.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return False

        return await self._s_repository.delete_subcategory(company_id=company_id, subcategory_id=subcategory_id)

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