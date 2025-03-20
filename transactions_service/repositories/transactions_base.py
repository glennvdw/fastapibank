from abc import ABC, abstractmethod
from typing import Optional, List
from models import Transaction

class ITransactionsRepository(ABC):
    @abstractmethod
    def save(self, account: Transaction) -> Transaction:
        """Persist or update a Transaction object."""
        pass

    @abstractmethod
    def filter(self, account_id: Optional[str] = None) -> List[Transaction]:
        """Filter transactions by account id"""
        pass