"""A module containing company category service."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.category import Category
from src.infrastructure.dto.categorydto import CategoryDTO

class ICategoryService(ABC):

    @abstractmethod
    async def get_all_categories(self) -> Iterable[CategoryDTO]:
        """The abstract getting all company categories from the repository.

        Returns:
            Iterable[CategoryDTO]: The collection of the all categories.
        """

    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> CategoryDTO | None:
        """The abstract getting a category from the repository.

        Args:
            category_id (int): The id of the category.

        Returns:
            Country | None: The category data if exists.
        """