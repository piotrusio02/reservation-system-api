"""A module containing category-related routers."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException


from src.container import Container
from src.infrastructure.dto.categorydto import CategoryDTO
from src.infrastructure.services.icategory import ICategoryService

router = APIRouter(tags=["Module 2: User, Companies and Categories"])

@router.get("/", response_model=Iterable[CategoryDTO], status_code=200)
@inject
async def get_categories(
        service: ICategoryService = Depends(Provide[Container.category_service]),
) -> Iterable:
    """An endpoint for getting all categories.

    Args:
        service (ICategoryService, optional): The injected service dependency.

    Returns:
        Iterable: All categories.
    """

    categories = await service.get_all_categories()

    return categories

@router.get("/{category_id}", response_model=CategoryDTO, status_code=200)
@inject
async def get_category_by_id(
        category_id: int,
        service: ICategoryService = Depends(Provide[Container.category_service]),
) -> dict:
    """An endpoint for getting category by id.

    Args:
        category_id (int): The id of the category.
        service (ICategoryService, optional): The injected service dependency.

    Returns:
        dict: The category details.
    """


    if category := await service.get_category_by_id(category_id=category_id):
        return category.model_dump()

    raise HTTPException(status_code=404, detail="Category not found")