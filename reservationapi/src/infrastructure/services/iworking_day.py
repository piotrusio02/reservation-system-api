"""A module containing working days company service."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.working_day import WorkingDayIn
from src.infrastructure.dto.working_daydto import WorkingDayDTO

class IWorkingDayService(ABC):
    """An abstract class for working days company service."""

    @abstractmethod
    async def create_update_day(self, account_id: UUID4, data: WorkingDayIn) -> WorkingDayDTO | None:
        """A method create or update a working day for company.

        Args:
            account_id (UUID4): The account id of the company.
            data (WorkingDayIn): The company working day information

        Returns:
            WorkingDayDTO | None: The working day DTO model.
        """

    @abstractmethod
    async def get_by_company_id(self, company_id: int) -> Iterable[WorkingDayDTO]:
        """The abstract getting working days for company by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[WorkingDayDTO]: The collection of the all day for company.
        """