"""Module containing company repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4

from src.core.domain.company import CompanyIn

class ICompanyRepository(ABC):
    """An abstract class representing protocol of company repository."""

    @abstractmethod
    async def create_company(self, account_id: UUID4, data: CompanyIn) -> Any | None:
        """The abstract creating new company

        Args:
            account_id (UUID4): The UUID4 of the account.
            data (CompanyIn): The company information

        Returns:
            Any: The newly created company object
        """

    @abstractmethod
    async def get_by_account_id(self, account_id: UUID4) -> Any | None:
        """The abstract getting user by provided account id.

        Args:
            account_id (UUID4): The id of the account.

        Returns:
            Any | None: The company account details
        """

    @abstractmethod
    async def get_by_id(self, company_id: int) -> Any | None:
        """The abstract getting company by provided id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Any | None: The company account details
        """

    @abstractmethod
    async def get_by_city_and_category(self, city: str, category_id: int) -> Iterable[Any]:
        """The abstract getting all company by city and category from the data storage.

        Args:
            city (str): City for filtering.
            category_id (int): The id of the category.

        Returns:
            Iterable[Any]: The collection of the all company by city and category.
        """

    @abstractmethod
    async def update_company(self, account_id: UUID4, data: CompanyIn) -> Any | None:
        """The abstract updating user information.

        Args:
            account_id (UUID4): The id of the account company.
            data (CompanyIn): The new Company information.

        Returns:
            Any | None: The updated company.
        """
