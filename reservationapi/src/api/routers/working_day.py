"""A module containing working day company-related routers."""

from typing import Iterable

from pydantic import UUID4
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.infrastructure.utils import consts
from src.core.domain.working_day import WorkingDayIn, WeekDay
from src.infrastructure.dto.working_daydto import WorkingDayDTO
from src.infrastructure.services.iworking_day import IWorkingDayService

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Module 3: Company Working Days"])

@router.post("", response_model=WorkingDayDTO, status_code=201)
@inject
async def create_update_working_day(
        day: WorkingDayIn,
        service: IWorkingDayService = Depends(Provide[Container.working_day_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for creating new working day for company.

    Args:
        day (WorkingDayIn): The working day input data.
        service (IWorkingDayService, optional): The injected company service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The working day DTO details.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )

    account_uuid = token_payload.get("sub")

    if not account_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if (day.opening_time is None) != (day.closing_time is None):
        raise HTTPException(status_code=400, detail="Opening and closing must be provided or both must be null")

    if (day.opening_time is not None) and (day.opening_time == day.closing_time):
        raise HTTPException(status_code=400, detail="Opening and closing cannot be the same")

    new_day = await service.create_update_day(
        account_id=UUID4(account_uuid),
        data=day
    )

    if new_day:
        return new_day.model_dump()

    raise HTTPException(status_code=404, detail="Company not found")

@router.get("/{company_id}", response_model=Iterable[WorkingDayDTO], status_code=200)
@inject
async def get_working_day_by_company_id(
        company_id: int,
        service: IWorkingDayService = Depends(Provide[Container.working_day_service]),
) -> Iterable:
    """An endpoint for getting working days for company.

    Args:
        company_id (int): The id of the company.
        service (IWorkingDayService, optional): The injected company service.

    Returns:
        Iterable: All seven days for companies.
    """

    return await service.get_by_company_id(company_id=company_id)
