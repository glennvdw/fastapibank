from typing import Dict, List, Optional
from models import Transaction
from repositories.transactions_base import ITransactionsRepository

class InMemoryTransactionsRepository(ITransactionsRepository):
    def __init__(self):
        self._store: Dict[str, Transaction] = {}

    def save(self, transaction: Transaction) -> Transaction:
        self._store[transaction.id] = transaction
        return transaction

    def filter(self, account_id: Optional[str] = None) -> List[Transaction]:
        if account_id is None:
            return list(self._store.values())
        else:
            return [
                transaction
                for transaction in self._store.values()
                if transaction.account_id == account_id
            ]