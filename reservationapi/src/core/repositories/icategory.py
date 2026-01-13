"""Module containing category repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable


class ICategoryRepository(ABC):
    """An abstract class representing protocol of category repository."""

    @abstractmethod
    async def get_all_categories(self) -> Iterable[Any]:
        """The abstract getting all categories from the data storage.

        Returns:
            Iterable[Any]: The collection of the all categories.
        """

    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> Any | None:
        """The abstract getting a category from the data storage.

        Args:
            category_id (int): The id of the category.

        Returns:
            Any | None: The category data if exists.
        """
