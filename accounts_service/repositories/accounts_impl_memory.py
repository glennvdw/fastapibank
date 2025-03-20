from typing import Dict, List, Optional
from models import Account
from repositories.accounts_base import IAccountsRepository

class InMemoryAccountsRepository(IAccountsRepository):
    def __init__(self):
        self._store: Dict[str, Account] = {}

    def save(self, account: Account) -> Account:
        self._store[account.id] = account
        return account

    def find_by_id(self, account_id: str) -> Optional[Account]:
        return self._store.get(account_id)

    def filter(self, customer_id: Optional[str] = None) -> List[Account]:
        if customer_id is None:
            return list(self._store.values())
        else:
            return [
                account
                for account in self._store.values()
                if account.customer_id == customer_id
            ]