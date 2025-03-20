from datetime import datetime
from typing import Optional
from models import Transaction
from schemas import CreateTransactionRequest, TransactionType
from repositories.transactions_base import ITransactionsRepository
from exceptions import AccountNotFound
from settings import ACCOUNTS_SERVICE_URL
from ports.accounts_port import IAccountsPort
from threading import Lock

class TransactionService:
    def __init__(
        self, 
        transaction_repository: ITransactionsRepository,
        accounts_port: IAccountsPort
    ):
        self._transaction_repository: ITransactionsRepository = transaction_repository
        self._accounts_port: IAccountsPort = accounts_port
        self._transaction_lock = Lock()

    def calculate_balance(self, account_id: str):
        total = 0
        for transaction in self._transaction_repository.filter(account_id):
            if transaction.type != TransactionType.DEPOSIT.value:
                raise NotImplementedError("transaction type not implemented")
            total += transaction.amount
        return total

    def list_transactions(self, account_id: Optional[str]):
        return self._transaction_repository.filter(account_id=account_id)

    def create_transaction(self, request: CreateTransactionRequest):
        if request.type != TransactionType.DEPOSIT.value:
            raise NotImplementedError("transaction type not implemented")

        account = self._accounts_port.get_account(request.account_id)
        if account is None:
            raise AccountNotFound()

        with self._transaction_lock:
            # [placeholder] check if balance allows transaction

            # record transaction
            new_transaction = Transaction(
                amount=request.amount,
                message=request.message,
                type=request.type,
                counterparty_iban=request.counterparty_iban,
                timestamp=datetime.now(),
                account_id=request.account_id
            )
            self._transaction_repository.save(new_transaction)

            # calculate new balance
            new_balance = self.calculate_balance(request.account_id)

        # Update the accounts balance
        self._accounts_port.update_balance(
            request.account_id, 
            new_balance,
            new_transaction.timestamp, # can be used for concurrency control
        )

        return new_transaction
