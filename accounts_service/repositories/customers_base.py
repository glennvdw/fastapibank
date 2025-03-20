from abc import ABC, abstractmethod
from typing import Optional
from models import Customer

class ICustomersRepository(ABC):
    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        """Persist or update an Account object."""
        pass

    @abstractmethod
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        """Retrieve an Customer by its ID."""
        pass

    @abstractmethod
    def exists(self, customer_id: str) -> bool:
        """Check if a Customer exists."""
        pass
