from typing import Dict, Optional
from models import Customer
from .customers_base import ICustomersRepository

class InMemoryCustomersRepository(ICustomersRepository):
    def __init__(self):
        self._store: Dict[str, Customer] = {}

    def save(self, customer: Customer) -> Customer:
        self._store[customer.id] = customer
        return customer

    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        return self._store.get(customer_id)
    
    def exists(self, customer_id: str) -> bool:
        return customer_id in self._store
    
    def all(self):
        return list(self._store.values())
