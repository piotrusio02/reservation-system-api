"""A module containing company-related routers."""

from typing import Iterable

from pydantic import UUID4
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.infrastructure.utils import consts
from src.core.domain.company import CompanyIn
from src.infrastructure.dto.companydto import CompanyDTO, CompanyListDTO, CompanyPublicDTO
from src.infrastructure.services.icompany import ICompanyService
from src.core.domain.account import Role

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Module 2: User, Companies and Categories"])

@router.post("/", response_model=CompanyDTO, status_code=201)
@inject
async def create_company(
        company: CompanyIn,
        service: ICompanyService = Depends(Provide[Container.company_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for creating new company.

    Args:
        company (CompanyIn): The company input data.
        service (ICompanyService, optional): The injected company service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The company DTO details.
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

    if new_company := await service.create_company(
            account_id=UUID4(account_uuid),
            company=company
    ):
        return new_company.model_dump()

    raise HTTPException(
        status_code=400,
        detail="Could not create company",
    )

@router.get("/", response_model=Iterable[CompanyListDTO], status_code=200)
@inject
async def get_companies(
        city: str,
        category_id: int,
        service: ICompanyService = Depends(Provide[Container.company_service]),
) -> Iterable:
    """An endpoint for getting all filtered companies.

    Args:
        city (str): The city to filter companies by.
        category_id (int): The ID of the category to filter.
        service (ICompanyService, optional): The injected service dependency.

    Returns:
        Iterable: All filtered companies.
    """

    return await service.get_by_city_and_category(city=city, category_id=category_id)

@router.get("/me", response_model=CompanyDTO, status_code=200)
@inject
async def get_my_company(
        service: ICompanyService = Depends(Provide[Container.company_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for getting company data.

    Args:
        service (ICompanyService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The company details.
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

    if company := await service.get_by_account_id(account_id=UUID4(account_uuid)):
        return company.model_dump()

    raise HTTPException(status_code=404, detail="Company not found")

@router.get("/{company_id}", response_model=CompanyPublicDTO, status_code=200)
@inject
async def get_company(
        company_id: int,
        service: ICompanyService = Depends(Provide[Container.company_service])
) -> dict:
    """An endpoint for getting company data.

    Args:
        company_id (int): The id of the company.
        service (ICompanyService, optional): The injected service dependency.

    Returns:
        dict: The company details.
    """

    if company := await service.get_by_id(company_id=company_id):
        return company.model_dump()

    raise HTTPException(status_code=404, detail="Company not found")

@router.put("/me", response_model=CompanyDTO, status_code=200)
@inject
async def update_company(
        company: CompanyIn,
        service: ICompanyService = Depends(Provide[Container.company_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating company data.

    Args:
        company (CompanyIn): The updated company details.
        service (ICompanyService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The updated company details.
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

    updated_company = await service.update_company(
        account_id=UUID4(account_uuid),
        data=company
    )

    if updated_company:
        return updated_company.model_dump()

    raise HTTPException(status_code=404, detail="Company not found")

