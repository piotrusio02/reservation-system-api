"""A module containing company subcategory service."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.company_subcategory import SubcategoryIn
from src.infrastructure.dto.company_subcategorydto import SubcategoryDTO


class ICompanySubcategoryService(ABC):
    """An abstract class for company subcategory service."""

    @abstractmethod
    async def create_subcategory(self, account_id: UUID4, data: SubcategoryIn) -> SubcategoryDTO | None:
        """A method create a new subcategory.

        Args:
            account_id (UUID4): The account id of the company.
            data (SubcategoryIn): The subcategory input data.

        Returns:
            SubcategoryDTO | None: The subcategory DTO model.
        """

    @abstractmethod
    async def get_subcategories(self, account_id: UUID4) -> Iterable[SubcategoryDTO]:
        """The abstract getting all subcategories for company from the data storage.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            Iterable[SubcategoryDTO]: The collection of the all subcategories for company.
        """

    @abstractmethod
    async def get_subcategories_by_company_id(self, company_id: int) -> Iterable[SubcategoryDTO]:
        """The abstract getting all subcategories for company from the data storage.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[SubcategoryDTO]: The collection of the all subcategories for company.
        """

    @abstractmethod
    async def update_subcategory(self, account_id: UUID4, subcategory_id: int, data: SubcategoryIn) -> SubcategoryDTO | None:
        """The method updating subcategory data in the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            subcategory_id (int): The id of the subcategory.
            data (SubcategoryIn): The details of the updated subcategory.

        Returns:
            SubcategoryDTO | None: The subcategory DTO model.
        """

    @abstractmethod
    async def delete_subcategory(self, account_id: UUID4, subcategory_id: int) -> bool:
        """The method updating removing subcategory from the data storage.

        Args:
            account_id (UUID4): The account id of the company.
            subcategory_id (int): The id of the subcategory.

        Returns:
            bool: Success of the operation.
        """