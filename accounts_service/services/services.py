from datetime import datetime
from typing import Optional
from models import Customer, Account
from schemas import CreateAccountRequest
from repositories.accounts_base import IAccountsRepository
from repositories.customers_base import ICustomersRepository
from exceptions import CustomerNotFound, AccountNotFoundError

class AccountsService:
    def __init__(
        self, 
        accounts_repository: IAccountsRepository,
        customers_repository: ICustomersRepository,
    ):
        self._accounts_repository = accounts_repository
        self._customers_repository = customers_repository

    def get_account(self, account_id: str):
        return self._accounts_repository.find_by_id(account_id)

    def list_accounts(self, customer_id: Optional[str]):
        return self._accounts_repository.filter(customer_id=customer_id)

    def create_account(self, request: CreateAccountRequest):
        if not self._customers_repository.find_by_id(request.customer_id):
            raise CustomerNotFound(request.customer_id)

        new_account = Account(
            customer_id=request.customer_id,
            name=request.name,
            balance=0.0,
        )
        self._accounts_repository.save(new_account)

        return new_account

    def update_balance(
        self, 
        account_id: str, 
        new_balance: float, 
        timestamp: datetime
    ) -> Account:

        # TODO use timestamp (or better some kind of sequence number)
        #  to protect against out of order updates

        account = self._accounts_repository.find_by_id(account_id)
        if not account:
            raise AccountNotFoundError(f"Account {account_id} not found")

        account.balance = new_balance

        self._accounts_repository.save(account)
        return account