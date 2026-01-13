"""A module containing company service-related routers."""

from typing import Iterable

from pydantic import UUID4
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.infrastructure.utils import consts
from src.core.domain.company_service import CompanyServiceIn, CompanyServiceUpdateIn
from src.infrastructure.dto.company_servicedto import ServiceDTO, ServiceListDTO, ServicePublicDTO
from src.infrastructure.dto.employeedto import EmployeePublicDTO, EmployeeDTO
from src.infrastructure.services.icompany_service import ICompanyServiceService
from src.core.domain.account import Role

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Module 5: Company Subcategories and Services"])

@router.post("", response_model=ServiceDTO, status_code=201)
@inject
async def create_service(
        company_service: CompanyServiceIn,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new service

    Args:
        company_service (CompanyServiceIn): The company service input data.
        service (ICompanyServiceService): The injected "company service" service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The company service DTO details.
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

    if new_service := await service.create_service(
            account_id=UUID4(account_uuid),
            data=company_service
    ):
        return new_service.model_dump()

    raise HTTPException(status_code=400, detail="Could not create service. Time must be a multiple of 15, or subcategory not found.")

@router.get("/me", response_model=Iterable[ServiceListDTO], status_code=200)
@inject
async def get_my_services(
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting all service for company.

    Args:
        service (ICompanyServiceService): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: All services for company.
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

    return await service.get_services(account_id=UUID4(account_uuid))

@router.get("/company/{company_id}", response_model=Iterable[ServiceListDTO], status_code=200)
@inject
async def get_company_services(
        company_id: int,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
) -> Iterable:
    """An endpoint for getting all company services.

    Args:
        company_id (int): The id of the company.
        service (ICompanyServiceService): The injected service dependency.

    Returns:
        Iterable: All services for company.
    """

    services = await service.get_services_by_company_id(company_id=company_id)

    if services is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return services

@router.get("/company/{company_id}/subcategory/{subcategory_id}", response_model=Iterable[ServiceListDTO], status_code=200)
@inject
async def get_company_services_by_subcategory(
        company_id: int,
        subcategory_id: int,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
) -> Iterable:
    """An endpoint for getting all company services by subcategory.

    Args:
        company_id (int): The id of the company.
        subcategory_id (int): The id of the subcategory.
        service (ICompanyServiceService, optional): The injected service dependency.

    Returns:
        Iterable: All services for company.
    """

    services = await service.get_services_by_company_id_and_subcategory_id(company_id=company_id,
                                                                           subcategory_id=subcategory_id)

    return services

@router.get("/me/{service_id}", response_model=ServiceDTO, status_code=200)
@inject
async def get_service_by_id(
        service_id: int,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for getting service data.

    Args:
        service_id (int): The id of the company service.
        service (ICompanyServiceService, optional): The injected service dependency.

    Returns:
        dict: The company service details.
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

    if company_service := await service.get_service_by_id(service_id=service_id):
        return company_service.model_dump()

    raise HTTPException(status_code=404, detail="Service not found")

@router.get("/{service_id}", response_model=ServicePublicDTO, status_code=200)
@inject
async def get_service_by_id_public(
        service_id: int,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
) -> dict:
    """An endpoint for getting service public data.

    Args:
        service_id (int): The id of the company service.
        service (ICompanyServiceService, optional): The injected service dependency.

    Returns:
        dict: The company service details.
    """

    if company_service := await service.get_service_by_id_public(service_id=service_id):
        return company_service.model_dump()

    raise HTTPException(status_code=404, detail="Service not found")

@router.put("/{service_id}", response_model=ServiceDTO, status_code=200)
@inject
async def update_service(
        service_id: int,
        company_service: CompanyServiceUpdateIn,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating service data.

    Args:
        service_id (int): The id of the service.
        company_service (CompanyServiceUpdateIn): The updated service details.
        service (ICompanyServiceService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The updated service details.
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

    updated_service = await service.update_service(
        account_id=UUID4(account_uuid),
        service_id=service_id,
        data=company_service
    )

    if updated_service:
        return updated_service.model_dump()

    raise HTTPException(status_code=404, detail="Service not found")

@router.delete("/{service_id}", status_code=204)
@inject
async def delete_service(
        service_id: int,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for delete service data.

    Args:
        service_id (int): The id of the service.
        service (ICompanyServiceService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if service does not exist.
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

    if await service.delete_service(account_id=UUID4(account_uuid), service_id=service_id):
        return

    raise HTTPException(status_code=404, detail="Service not found")

@router.post("/{service_id}/employees/{employee_id}", status_code=201)
@inject
async def add_employee_to_service(
        service_id: int,
        employee_id: int,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> bool:
    """The method adding new employee to service.

    Args:
        service_id (int): The id of the service.
        employee_id (int): The id of the employee.
        service (ICompanyServiceService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        bool: Success of the operation.
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

    if await service.add_employee_to_service(
        account_id=UUID4(account_uuid),
        service_id=service_id,
        employee_id=employee_id
    ):
        return True

    raise HTTPException(status_code=400, detail="Assignment failed")

@router.get("/me/{service_id}/employees", response_model=Iterable[EmployeeDTO], status_code=200)
@inject
async def get_service_employees(
        service_id: int,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Iterable:
    """An endpoint for getting all service employees.

    Args:
        service_id (int): The id of the service.
        service (ICompanyServiceService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: All employee assigned to service.
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


    employees = await service.get_designed_employees(account_id=UUID4(account_uuid),
                                                     service_id=service_id)

    return employees

@router.get("/{service_id}/employees", response_model=Iterable[EmployeePublicDTO], status_code=200)
@inject
async def get_service_employees_public(
        service_id: int,
        service: ICompanyServiceService = Depends(Provide[Container.service_service])
) -> Iterable:
    """An endpoint for getting all service employees public data.

    Args:
        service_id (int): The id of the service.
        service (ICompanyServiceService, optional): The injected service dependency.

    Returns:
        Iterable: All employee assigned to service.
    """

    employees = await service.get_designed_employees_public(service_id=service_id)

    return employees

@router.delete("/{service_id}/employees/{employee_id}", status_code=204)
@inject
async def remove_employee_from_service(
        service_id: int,
        employee_id: int,
        service: ICompanyServiceService = Depends(Provide[Container.service_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for delete employee from service data.

    Args:
        service_id (int): The id of the service.
        employee_id (int): The id of the employee.
        service (ICompanyServiceService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if service does not exist.
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

    if await service.remove_employee_from_service(
        account_id=UUID4(account_uuid),
        service_id=service_id,
        employee_id=employee_id
    ):
        return

    raise HTTPException(status_code=404, detail="Service or employee not found")