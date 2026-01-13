"""Module containing working days company repository database implementation."""

from typing import Any, Iterable

from sqlalchemy.dialects.postgresql import insert

from src.core.domain.working_day import WorkingDayIn
from src.core.repositories.iworking_day import IWorkingDayRepository
from src.db import working_day_table, database

class WorkingDayRepository(IWorkingDayRepository):
    """A class implementing the database  working days company repository."""

    async def create_update_day(self, company_id: int, data: WorkingDayIn) -> Any | None:
        """The abstract creating or updating new working day for company

        Args:
            company_id (int): The id of the company.
            data (WorkingDayIn): The company working day information

        Returns:
            Any: The newly created day object
        """

        insert_data = {
            "company_id": company_id,
            "day": data.day.value,
            "opening_time": data.opening_time,
            "closing_time": data.closing_time,
        }

        insert_stmt = insert(working_day_table).values(**insert_data)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint="uix_1",
            set_={
                "opening_time": insert_stmt.excluded.opening_time,
                "closing_time": insert_stmt.excluded.closing_time,
            }
        ).returning(working_day_table)

        return await database.fetch_one(do_update_stmt)

    async def get_by_company_id(self, company_id: int) -> Iterable[Any]:
        """The abstract getting working days for company by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[Any]: The collection of the all day for company.
        """

        query = (
            working_day_table.select()
            .where(working_day_table.c.company_id == company_id)
        )

        return await database.fetch_all(query)