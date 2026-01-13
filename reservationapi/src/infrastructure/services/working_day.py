"""A module containing working days company service."""

from typing import Iterable

from pydantic import UUID4

from src.core.domain.working_day import WorkingDayIn, WeekDay
from src.core.repositories.iworking_day import IWorkingDayRepository
from src.core.repositories.icompany import ICompanyRepository
from src.infrastructure.dto.working_daydto import WorkingDayDTO
from src.infrastructure.services.iworking_day import IWorkingDayService

class WorkingDayService(IWorkingDayService):
    """A class implementing the working days company service."""

    _wd_repository: IWorkingDayRepository
    _c_repository: ICompanyRepository


    def __init__(self, wd_repository: IWorkingDayRepository, c_repository: ICompanyRepository) -> None:
        """The initializer of the working dat company service.

        Args:
            wd_repository (IWorkingDayRepository): The reference to the working day repository.
            c_repository (ICompanyRepository): The reference to the company repository.
        """

        self._wd_repository = wd_repository
        self._c_repository = c_repository

    async def create_update_day(self, account_id: UUID4, data: WorkingDayIn) -> WorkingDayDTO | None:
        """A method create or update a working day for company.

        Args:
            account_id (UUID4): The account id of the company.
            data (WorkingDayIn): The company working day information

        Returns:
            WorkingDayDTO | None: The working day DTO model.
        """

        company_id = await self._get_company_id(account_id)
        if not company_id:
            return None

        if (data.opening_time is None) != (data.closing_time is None):
            return None

        if data.opening_time is not None:
            if data.opening_time == data.closing_time:
                return None

        updated = await self._wd_repository.create_update_day(company_id, data)
        if not updated:
            return None

        updated = dict(updated)
        updated["day"] = updated["day"].value

        return WorkingDayDTO(**dict(updated))


    async def get_by_company_id(self, company_id: int) -> Iterable[WorkingDayDTO]:
        """The method getting working days for company by provided company id.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[WorkingDayDTO]: The collection of the all day for company.
        """

        existing_days = dict()
        seven_days_list = list()

        days = await self._wd_repository.get_by_company_id(company_id)

        for day in days:
            day_enum = day["day"]

            day_dict = dict(day)
            day_dict["day"] = day_enum.value
            existing_days[day_enum.value] = WorkingDayDTO(**day_dict)

        for day_enum in WeekDay:
            if day_enum.value in existing_days:
                seven_days_list.append(existing_days[day_enum.value])

            else:
                default = {
                    "id": None,
                    "day": day_enum.value,
                    "opening_time": None,
                    "closing_time": None,
                }
                seven_days_list.append(WorkingDayDTO(**default))

        return seven_days_list


    async def _get_company_id(self, account_id: UUID4) -> int | None:
        """A private method translating account ID to company ID.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            int | None: The company ID
        """

        company = await self._c_repository.get_by_account_id(account_id)

        if not company:
            return None

        return company["id"]
