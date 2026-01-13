"""A module containing reservation-related routers."""

from typing import Iterable
from datetime import datetime, date

from pydantic import UUID4
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.infrastructure.utils import consts
from src.core.domain.reservation import ReservationIn, ReservationStatusUpdateIn, ReservationStatus
from src.infrastructure.dto.reservationdto import ReservationDTO, ReservationListDTO
from src.infrastructure.services.ireservation import IReservationService
from src.core.domain.account import Role

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Module 6: Reservations"])

@router.post("", response_model=ReservationDTO, status_code=201)
@inject
async def create_reservation(
        reservation: ReservationIn,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for creating new reservation.

    Args:
        reservation (ReservationIn): The reservation input data.
        service (IReservationService): The injected reservation service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The reservation DTO details.
    """
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )

    account_uuid = token_payload.get("sub")
    account_role = token_payload.get("role")

    if not account_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if account_role != Role.USER.value and account_role != Role.COMPANY.value:
        raise HTTPException(status_code=403, detail="Unauthorized")

    new_reservation = await service.create_reservation(account_id=UUID4(account_uuid), role=account_role, data=reservation)

    if new_reservation:
        return new_reservation.model_dump()

    raise HTTPException(status_code=400, detail="Could not create reservation")

@router.get("/available", response_model=Iterable[datetime], status_code=200)
@inject
async def get_available_slots(
        employee_id: int,
        service_id: int,
        day: date,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """An endpoint for getting available slots for service.

    Args:
        employee_id (int): The id of the employee.
        service_id (int): The id of the company service.
        day (date): The day to check available slots.
        service (IReservationService, optional): The injected service dependency.

    Returns:
        Iterable: All available slots for service and employee.
    """

    slots = await service.get_available_slots_service(employee_id=employee_id, service_id=service_id, day=day)

    if slots is None:
        raise HTTPException(status_code=404, detail="Service or employee not found or employee is not assigned")

    return slots

@router.get("/client", response_model=Iterable[ReservationListDTO], status_code=200)
@inject
async def get_client_reservations(
        service: IReservationService = Depends(Provide[Container.reservation_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting all reservations for client.

    Args:
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: All reservations for client.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )

    account_uuid = token_payload.get("sub")
    account_role = token_payload.get("role")

    if not account_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if account_role != Role.USER.value:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return await service.get_client_reservations(account_id=UUID4(account_uuid))

@router.get("/company", response_model=Iterable[ReservationListDTO], status_code=200)
@inject
async def get_company_reservations(
        service: IReservationService = Depends(Provide[Container.reservation_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting all reservations for company.

    Args:
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: All reservations for company.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )

    account_uuid = token_payload.get("sub")
    account_role = token_payload.get("role")

    if not account_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if account_role != Role.COMPANY.value:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return await service.get_company_reservations(account_id=UUID4(account_uuid))

@router.get("/company/{employee_id}", response_model=Iterable[ReservationListDTO], status_code=200)
@inject
async def get_company_reservations_by_employee(
        employee_id: int,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting all reservations for company by employee.

    Args:
        employee_id (int): The id of the employee.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: All reservations for company.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )

    account_uuid = token_payload.get("sub")
    account_role = token_payload.get("role")

    if not account_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if account_role != Role.COMPANY.value:
        raise HTTPException(status_code=403, detail="Unauthorized")

    reservations = await service.get_employee_reservations(account_id=UUID4(account_uuid),
                                                              employee_id=employee_id)

    if reservations is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return reservations

@router.get("/{reservation_id}", response_model=ReservationDTO, status_code=200)
@inject
async def get_reservation_by_id(
        reservation_id: int,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for getting reservation data.

    Args:
        reservation_id (int): The id of the reservation.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The reservation details.
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

    if reservation := await service.get_reservation_by_id(account_id=UUID4(account_uuid),
                                                          reservation_id=reservation_id):
        return reservation.model_dump()

    raise HTTPException(status_code=404, detail="Reservation not found")

@router.patch("/{reservation_id}", response_model=ReservationDTO, status_code=200)
@inject
async def update_reservation_status(
        reservation_id: int,
        reservation_status: ReservationStatusUpdateIn,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating reservation status data.

    Args:
        reservation_id (int): The id of the reservation.
        reservation_status (ReservationStatusUpdateIn): The updated status details.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The updated reservation status details.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )

    account_uuid = token_payload.get("sub")
    account_role = token_payload.get("role")

    if not account_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if account_role != Role.COMPANY.value:
        raise HTTPException(status_code=403, detail="Unauthorized")

    reservation = await service.get_reservation_by_id(account_id=account_uuid, reservation_id=reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.status == ReservationStatus.COMPLETED.value or reservation.status == ReservationStatus.CANCELLED.value:
        raise HTTPException(status_code=400, detail="Status is completed or cancelled. Cannot be updated")

    updated_reservation = await service.update_reservation_status(
        account_id=UUID4(account_uuid),
        reservation_id=reservation_id,
        data=reservation_status
    )

    if updated_reservation:
        return updated_reservation.model_dump()

    raise HTTPException(status_code=400, detail="Update failed")
