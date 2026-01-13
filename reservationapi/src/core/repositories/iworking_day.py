"""Module containing working days company repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable


from src.core.domain.working_day import WorkingDayIn

class IWorkingDayRepository(ABC):
    """An abstract class representing protocol of user repository."""

    @abstractmethod
    async def create_update_day(self, company_id: int, data: WorkingDayIn) -> Any | None:
        """The abstract creating or updating new working day for company

        Args:
            company_id (int): The id of the company.
            data (WorkingDayIn): The company working day information

        Returns:
            Any: The newly created day object
        """

    @abstractmethod
    async def get_by_company_id(self, company_id: int) -> Iterable[Any]:
        """The abstract getting working days for company by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[Any]: The collection of the all day for company.
        """