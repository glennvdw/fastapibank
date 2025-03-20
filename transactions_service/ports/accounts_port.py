from abc import ABC, abstractmethod
from typing import Optional
from schemas import AccountResponse
from datetime import datetime

class IAccountsPort(ABC):
    @abstractmethod
    def get_account(self, account_id: str) -> Optional[AccountResponse]:
        pass

    @abstractmethod
    def update_balance(
        self, 
        account_id: str, 
        new_balance: float,
        timestamp: datetime,
    ):
        pass