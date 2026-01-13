"""A module containing company subcategory-related routers."""

from typing import Iterable

from pydantic import UUID4
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.infrastructure.utils import consts
from src.core.domain.company_subcategory import SubcategoryIn
from src.infrastructure.dto.company_subcategorydto import SubcategoryDTO
from src.infrastructure.services.icompany_subcategory import ICompanySubcategoryService
from src.core.domain.account import Role

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Module 5: Company Subcategories and Services"])

@router.post("", response_model=SubcategoryDTO, status_code=201)
@inject
async def create_subcategory(
        subcategory: SubcategoryIn,
        service: ICompanySubcategoryService = Depends(Provide[Container.subcategory_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding a new subcategory.

    Args:
        subcategory (SubcategoryIn): The subcategory input data.
        service (ICompanySubcategoryService, optional): The injected subcategory service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The subcategory DTO details.
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

    if new_subcategory := await service.create_subcategory(
            account_id=UUID4(account_uuid),
            data=subcategory
    ):
        return new_subcategory.model_dump()

    raise HTTPException(status_code=400, detail="Could not create subcategory")

@router.get("/me", response_model=Iterable[SubcategoryDTO], status_code=200)
@inject
async def get_my_subcategories(
        service: ICompanySubcategoryService = Depends(Provide[Container.subcategory_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting all subcategories for company.

    Args:
        service (ICompanySubcategoryService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: All subcategories for company.
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

    return await service.get_subcategories(account_id=UUID4(account_uuid))

@router.get("/company/{company_id}", response_model=Iterable[SubcategoryDTO], status_code=200)
@inject
async def get_company_subcategories(
        company_id: int,
        service: ICompanySubcategoryService = Depends(Provide[Container.subcategory_service]),
) -> Iterable:
    """An endpoint for getting all company subcategories.

    Args:
        company_id (int): The id of the company.
        service (ICompanySubcategoryService, optional): The injected service dependency.

    Returns:
        Iterable: All subcategories for company.
    """

    subcategories = await service.get_subcategories_by_company_id(company_id=company_id)

    return subcategories

@router.put("/{subcategory_id}", response_model=SubcategoryDTO, status_code=200)
@inject
async def update_subcategory(
        subcategory_id: int,
        subcategory: SubcategoryIn,
        service: ICompanySubcategoryService = Depends(Provide[Container.subcategory_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating subcategory data.

    Args:
        subcategory_id (int): The id of the subcategory.
        subcategory (SubcategoryIn): The updated subcategory details.
        service (ICompanySubcategoryService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The updated subcategory details.
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

    updated_subcategory = await service.update_subcategory(
        account_id=UUID4(account_uuid),
        subcategory_id=subcategory_id,
        data=subcategory
    )

    if updated_subcategory:
        return updated_subcategory.model_dump()

    raise HTTPException(status_code=404, detail="Subcategory not found")

@router.delete("/{subcategory_id}", status_code=204)
@inject
async def delete_subcategory(
        subcategory_id: int,
        service: ICompanySubcategoryService = Depends(Provide[Container.subcategory_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for delete subcategory data.

    Args:
        subcategory_id (int): The id of the subcategory.
        service (ICompanySubcategoryService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if subcategory does not exist.
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

    if await service.delete_subcategory(account_id=UUID4(account_uuid), subcategory_id=subcategory_id):
        return

    raise HTTPException(status_code=404, detail="Subcategory not found")