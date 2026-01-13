"""A module containing employee-related routers."""

from typing import Iterable

from pydantic import UUID4
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.infrastructure.utils import consts
from src.core.domain.employee import EmployeeIn
from src.infrastructure.dto.employeedto import EmployeeDTO, EmployeePublicDTO
from src.infrastructure.services.iemployee import IEmployeeService
from src.core.domain.account import Role

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Module 4: Employees"])

@router.post("", response_model=EmployeeDTO, status_code=201)
@inject
async def create_employee(
        employee: EmployeeIn,
        service: IEmployeeService = Depends(Provide[Container.employee_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for creating new employee.

    Args:
        employee (EmployeeIn): The employee input data.
        service (IEmployeeService, optional): The injected employee service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The employee DTO details.
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

    if new_employee := await service.create_employee(
            account_id=UUID4(account_uuid),
            data=employee
    ):
        return new_employee.model_dump()

    raise HTTPException(status_code=400, detail="Could not create employee")

@router.get("/me", response_model=Iterable[EmployeeDTO], status_code=200)
@inject
async def get_my_employees(
        service: IEmployeeService = Depends(Provide[Container.employee_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting all employees for company.

    Args:
        service (IEmployeeService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: All employees for company.
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

    return await service.get_employees(account_id=UUID4(account_uuid))

@router.get("/company/{company_id}", response_model=Iterable[EmployeePublicDTO], status_code=200)
@inject
async def get_company_employees(
        company_id: int,
        service: IEmployeeService = Depends(Provide[Container.employee_service]),
) -> Iterable:
    """An endpoint for getting all company employees.

    Args:
        company_id (int): The id of the company.
        service (IEmployeeService, optional): The injected service dependency.

    Returns:
        Iterable: All employees for company.
    """

    employees = await service.get_employees_by_company_id(company_id=company_id)

    return employees

@router.get("/{employee_id}", response_model=EmployeeDTO, status_code=200)
@inject
async def get_employee(
        employee_id: int,
        service: IEmployeeService = Depends(Provide[Container.employee_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for getting employee data.

    Args:
        employee_id (int): The id of the employee.
        service (IEmployeeService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The employee details.
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

    if employee := await service.get_employee_by_id(
            account_id=UUID4(account_uuid),
            employee_id=employee_id
    ):
        return employee.model_dump()

    raise HTTPException(status_code=404, detail="Employee not found")

@router.put("/{employee_id}", response_model=EmployeeDTO, status_code=200)
@inject
async def update_employee(
        employee_id: int,
        employee: EmployeeIn,
        service: IEmployeeService = Depends(Provide[Container.employee_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating employee data.

    Args:
        employee_id (int): The id of the employee.
        employee (EmployeeIn): The updated employee details.
        service (IEmployeeService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The updated employee details.
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

    updated_employee = await service.update_employee(
        account_id=UUID4(account_uuid),
        employee_id=employee_id,
        data=employee
    )

    if updated_employee:
        return updated_employee.model_dump()

    raise HTTPException(status_code=404, detail="Employee not found")

@router.delete("/{employee_id}", status_code=204)
@inject
async def delete_employee(
        employee_id: int,
        service: IEmployeeService = Depends(Provide[Container.employee_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting employee data.

    Args:
        employee_id (int): The id of the employee.
        service (IEmployeeService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if employee does not exist.
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

    if await service.delete_employee(account_id=UUID4(account_uuid), employee_id=employee_id):
        return

    raise HTTPException(status_code=404, detail="Employee not found")
