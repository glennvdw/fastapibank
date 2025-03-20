from abc import ABC, abstractmethod
from typing import Optional, List
from models import Account

class IAccountsRepository(ABC):
    @abstractmethod
    def save(self, account: Account) -> Account:
        """Persist or update an Account object."""
        pass

    @abstractmethod
    def find_by_id(self, account_id: str) -> Optional[Account]:
        """Retrieve an Account by its ID."""
        pass

    @abstractmethod
    def filter(self, customer_id: Optional[str] = None) -> List[Account]:
        """Filter accounts by customer id"""
        pass