"""A module containing user-related routers."""

from pydantic import UUID4
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.infrastructure.utils import consts
from src.core.domain.user import UserIn
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.iuser import IUserService
from src.core.domain.account import Role

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Module 2: User, Companies and Categories"])

@router.post("/", response_model=UserDTO, status_code=201)
@inject
async def create_user(
        user: UserIn,
        service: IUserService = Depends(Provide[Container.user_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for creating new user.

    Args:
        user (UserIn): The user input data.
        service (IUserService, optional): The injected user service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The user DTO details.
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

    if new_user := await service.create_user(
            account_id=UUID4(account_uuid),
            user=user
    ):
        return new_user.model_dump()

    raise HTTPException(
        status_code=400,
        detail="The user with provided account already exists",
    )

@router.get("/me", response_model=UserDTO, status_code=200)
@inject
async def get_me(
        service: IUserService = Depends(Provide[Container.user_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for getting user data.

    Args:
        service (IUserService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The user details.
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

    if user := await service.get_by_account_id(account_id=UUID4(account_uuid)):
        return user.model_dump()

    raise HTTPException(status_code=404, detail="User not found")


@router.put("/me", response_model=UserDTO, status_code=200)
@inject
async def update_user(
        user: UserIn,
        service: IUserService = Depends(Provide[Container.user_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating user data.

    Args:
        user (UserIn): The updated user details.
        service (IUserService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The updated user details.
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

    updated_user = await service.update_user(
        account_id=UUID4(account_uuid),
        data=user
    )

    if updated_user:
        return updated_user.model_dump()

    raise HTTPException(status_code=404, detail="User not found")