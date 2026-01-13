"""A module containing account-related routers."""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.infrastructure.utils import consts
from src.core.domain.account import AccountIn, LoginIn, PasswordUpdateIn
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.dto.accountdto import AccountDTO
from src.infrastructure.services.iaccount import IAccountService

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Module 1: Authentication and Login"])




@router.post("/register", response_model=AccountDTO, status_code=201)
@inject
async def register_account(
        account: AccountIn,
        service: IAccountService = Depends(Provide[Container.account_service]),
) -> dict:
    """A router coroutine for registering new account.

    Args:
        account (AccountIn): The account input data.
        service (IAccountService, optional): The injected account service.

    Returns:
        dict: The account DTO details.
    """

    if new_account := await service.register_account(account):
        return new_account.model_dump()

    raise HTTPException(
        status_code=400,
        detail="The user with provided e-mail already exists",
    )

@router.post("/token", response_model=TokenDTO, status_code=200)
@inject
async def authenticate_account(
        account: LoginIn,
        service: IAccountService = Depends(Provide[Container.account_service]),
) -> dict:
    """A router coroutine for authenticating account.

    Args:
        account (LoginIn): The account input data.
        service (IAccountService, optional): The injected account service.

    Returns:
        dict: The token DTO details.
    """

    if token_details := await service.authenticate_account(account):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(
        status_code=401,
        detail="Provided incorrect credentials",
    )

@router.patch("/password",
              response_model=AccountDTO,
              status_code=200)
@inject
async def update_password(
        account_password: PasswordUpdateIn,
        service: IAccountService = Depends(Provide[Container.account_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """A router coroutine for updating password.

    Args:
        account_password (PasswordUpdateIn): The account input data.
        service (IAccountService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The account DTO details.
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


    updated_password = await service.update_password(
        uuid=account_uuid,
        old_password=account_password.old_password,
        new_password=account_password.new_password
    )
    if not updated_password:
        raise HTTPException(status_code=400, detail="Incorrect old password")

    return updated_password.model_dump()
