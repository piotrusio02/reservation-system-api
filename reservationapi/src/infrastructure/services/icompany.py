"""A module containing company service."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.company import CompanyIn
from src.infrastructure.dto.companydto import CompanyDTO

class ICompanyService(ABC):
    """An abstract class for company service."""

    @abstractmethod
    async def create_company(self, account_id: UUID4, company: CompanyIn) -> CompanyDTO | None:
        """A method create a new company.

        Args:
            account_id (UUID4): The account id of the company.
            company (CompanyIn): The company input data.

        Returns:
            CompanyDTO | None: The company DTO model.
        """

    @abstractmethod
    async def get_by_account_id(self, account_id: UUID4) -> CompanyDTO | None:
        """A method getting company by account id.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            CompanyDTO | None: The company data, if found.
        """

    @abstractmethod
    async def get_by_id(self, company_id: int) -> CompanyDTO | None:
        """A method getting company by account id.

        Args:
            company_id (int): The id of the company.

        Returns:
            CompanyDTO | None: The company data, if found.
        """

    @abstractmethod
    async def get_by_city_and_category(self, city: str, category_id: int) -> Iterable[CompanyDTO]:
        """The abstract getting all company by city and category from the data storage.

        Args:
            city (str): City for filtering.
            category_id (int): The id of the category.

        Returns:
            Iterable[CompanyDTO]: The collection of the all company by city and category.
        """

    @abstractmethod
    async def update_company(self, account_id: UUID4, data: CompanyIn) -> CompanyDTO | None:
        """The method updating company data in the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            data (CompanyIn): The details of the updated company info.

        Returns:
            CompanyDTO | None: The updated company details.
        """
