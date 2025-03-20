from fastapi import Depends
from repositories.accounts_base import IAccountsRepository
from repositories.customers_base import ICustomersRepository
from repositories.accounts_impl_memory import InMemoryAccountsRepository
from repositories.customers_impl_memory import InMemoryCustomersRepository
from services.services import AccountsService
from models import Customer, Account

accounts_repository = InMemoryAccountsRepository()
customers_repository = InMemoryCustomersRepository()

customers_repository.save(customer=Customer(id="cus-001", name="Eddy", surname="unknown"))
customers_repository.save(customer=Customer(id="cus-002", name="Pieter-Jan", surname="unknown"))

accounts_repository.save(account=Account(
    id="acc-1",
    customer_id="cus-001",
    name="test account",
    balance=0
))

def get_accounts_repository() -> IAccountsRepository:
    """
    Return the global (singleton) repository instance.

    ! beware of thread safety
    """
    return accounts_repository


def get_customers_repository() -> IAccountsRepository:
    """
    Return the global (singleton) repository instance.

    ! beware of thread safety
    """
    return customers_repository


def get_accounts_service(
    accounts: IAccountsRepository = Depends(get_accounts_repository),
    customers: ICustomersRepository = Depends(get_customers_repository),
) -> AccountsService:
    return AccountsService(
        accounts_repository=accounts, 
        customers_repository=customers
    )