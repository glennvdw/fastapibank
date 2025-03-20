from fastapi import Depends
from repositories.transactions_base import ITransactionsRepository
from repositories.transactions_impl_memory import InMemoryTransactionsRepository
from services.services import TransactionService
from ports.accounts_port import IAccountsPort
from adapters.accounts_client import AccountsClient
from models import Transaction

transactions_repository = InMemoryTransactionsRepository()

def get_transactions_repository() -> ITransactionsRepository:
    """
    Return the global (singleton) repository instance.

    ! beware of thread safety
    """
    return transactions_repository


def get_accounts_port() -> IAccountsPort:
    return AccountsClient()


def get_transaction_service(
    transactions: ITransactionsRepository = Depends(get_transactions_repository),
    accounts_port: IAccountsPort = Depends(get_accounts_port)
) -> TransactionService:
    return TransactionService(
        transaction_repository=transactions,
        accounts_port=accounts_port
    )
