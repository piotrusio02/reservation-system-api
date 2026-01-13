"""Module containing company subcategory repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from src.core.domain.company_subcategory import SubcategoryIn

class ICompanySubcategoryRepository(ABC):
    """An abstract class representing protocol of company subcategory repository."""

    @abstractmethod
    async def create_subcategory(self, company_id: int, data: SubcategoryIn) -> Any | None:
        """The abstract creating new company subcategory

        Args:
            company_id (int): The id of the company.
            data (SubcategoryIn): The attributes of the new subcategory

        Returns:
            Any: The newly created subcategory object
        """

    @abstractmethod
    async def get_subcategories_by_company_id(self, company_id: int) -> Iterable[Any] | None:
        """The abstract getting all subcategories by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Any | None: The collection of the all subcategories for company.
        """

    @abstractmethod
    async def update_subcategory(self, company_id: int, subcategory_id: int, data: SubcategoryIn) -> Any | None:
        """The abstract updating subcategory information.

        Args:
            company_id (int): The id of the company.
            subcategory_id (int): The id of the subcategory.
            data (SubcategoryIn): The new subcategory information

        Returns:
            Any | None: The updated subcategory.
        """

    @abstractmethod
    async def delete_subcategory(self, company_id: int, subcategory_id: int) -> bool:
        """The abstract updating removing subcategory from the data storage.

        Args:
            company_id (int): The id of the company.
            subcategory_id (int): The subcategory id.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_subcategory_by_id(self, company_id: int, subcategory_id: int) -> Any | None:
        """The method getting an employee from the data storage.

        Args:`
            company_id (int): The id of the company.
            subcategory_id (int): The id of the subcategory.

        Returns:
            Any | None: The subcategory data if exists.
        """