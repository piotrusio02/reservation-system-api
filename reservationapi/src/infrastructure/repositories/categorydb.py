"""Module containing company category repository database implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore

from src.core.repositories.icategory import ICategoryRepository
from src.db import category_table, database


class CategoryRepository(ICategoryRepository):
    """A class implementing the database category repository."""

    async def get_all_categories(self) -> Iterable[Any]:
        """The abstract getting all categories from the data storage.

        Returns:
            Iterable[Any]: The collection of the all categories.
        """

        query = category_table.select().order_by(category_table.c.id.asc())
        return await database.fetch_all(query)


    async def get_category_by_id(self, category_id: int) -> Any | None:
        """A method getting account by id.

        Args:
            category_id (int): The id of the category.

        Returns:
            Any | None: The country data if exists.
        """

        query = (
            category_table.select()
            .where(category_table.c.id == category_id)
        )
        return await database.fetch_one(query)

