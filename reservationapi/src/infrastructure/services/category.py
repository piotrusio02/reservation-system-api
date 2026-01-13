"""Module containing company category service implementation."""

from typing import Iterable

from src.core.domain.category import Category
from src.core.repositories.icategory import ICategoryRepository
from src.infrastructure.dto.categorydto import CategoryDTO
from src.infrastructure.services.icategory import ICategoryService


class CategoryService(ICategoryService):
    """A class implementing the category service."""

    _repository: ICategoryRepository

    def __init__(self, repository: ICategoryRepository) -> None:
        """The initializer of the `category service`.

        Args:
            repository (ICategoryRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_categories(self) -> Iterable[CategoryDTO]:
        """The abstract getting all categories from the repository.

        Returns:
            Iterable[CategoryDTO]: The collection of the all categories.
        """

        categories = await self._repository.get_all_categories()

        return [CategoryDTO(**dict(category)) for category in categories]

    async def get_category_by_id(self, category_id: int) -> CategoryDTO | None:
        """The abstract getting a company category from the repository.

        Args:
            category_id (int): The id of the category.

        Returns:
            CategoryDTO | None: The category data if exists.
        """

        category = await self._repository.get_category_by_id(category_id)

        return CategoryDTO(**dict(category)) if category else None
