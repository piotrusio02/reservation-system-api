"""A module containing helper functions for token generation."""

from datetime import datetime, timedelta, timezone

from jose import jwt
from pydantic import UUID4

from src.infrastructure.utils.consts import (
    EXPIRATION_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)


def generate_account_token(account_uuid: UUID4, account_role: str) -> dict:
    """A function returning JWT token for account.

    Args:
        account_uuid (UUID5): The UUID of the account.
        account_role (str): The account role (user or company).

    Returns:
        dict: The token details.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    jwt_data = {"sub": str(account_uuid), "role": account_role, "exp": expire, "type": "confirmation"}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)

    return {"user_token": encoded_jwt, "expires": expire}