"""A module containing account service."""

from pydantic import UUID4

from src.core.domain.account import AccountIn, LoginIn
from src.core.repositories.iaccount import IAccountRepository
from src.infrastructure.dto.accountdto import AccountDTO
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.services.iaccount import IAccountService
from src.infrastructure.utils.password import verify_password
from src.infrastructure.utils.token import generate_account_token

class AccountService(IAccountService):
    """An abstract class for account service."""

    _repository: IAccountRepository

    def __init__(self, repository: IAccountRepository) -> None:
        self._repository = repository

    async def register_account(self, account: AccountIn) -> AccountDTO | None:
        """A method registering a new account.

        Args:
            account (AccountIn): The account input data.

        Returns:
            AccountDTO | None: The account DTO model.
        """

        account_record = await self._repository.register_account(account)

        if account_record:
            return AccountDTO(**dict(account_record))
        return None

    async def authenticate_account(self, account: LoginIn) -> TokenDTO | None:
        """The method authenticating the account.

        Args:
            account (LoginIn): The account data.

        Returns:
            TokenDTO | None: The token details.
        """

        if account_data := await self._repository.get_by_email(account.email):
            if verify_password(account.password, account_data.password):
                account_role = account_data.role.value
                token_details = generate_account_token(account_data.id, account_role=account_role)
                # trunk-ignore(bandit/B106)
                return TokenDTO(token_type="Bearer", **token_details)

            return None

        return None

    async def update_password(self, uuid: UUID4, old_password: str, new_password: str) -> AccountDTO | None:
        """A method updating password for account.

        Args:
            uuid (UUID4): UUID of the account.
            old_password (str): old password.
            new_password (str): new password.

        Returns:
            Any | None: The account object if exists.
        """
        if account_data := await self._repository.get_account_by_uuid(uuid):
            if verify_password(old_password, account_data.password):
                updated_password = await self._repository.update_password(uuid, new_password)
                return AccountDTO(**dict(updated_password))

            return None

        return None

    async def get_by_uuid(self, uuid: UUID4) -> AccountDTO | None:
        """A method getting account by UUID.

        Args:
            uuid (UUID4): The UUID of the account.

        Returns:
            AccountDTO | None: The updated account data, if successful.
        """

        account = await self._repository.get_account_by_uuid(uuid)
        if account:
            return AccountDTO(**dict(account))
        return None

    async def get_by_email(self, email: str) -> AccountDTO | None:
        """A method getting account by email.

        Args:
            email (str): The email of the account.

        Returns:
            AccountDTO | None: The account data, if found.
        """

        account = await self._repository.get_by_email(email)
        if account:
            return AccountDTO(**dict(account))
        return None