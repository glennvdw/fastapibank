from typing import List
from pydantic import BaseModel, Field
from uuid import uuid4

class Account(BaseModel):
    id: str = Field(default_factory=lambda _: uuid4().hex)
    customer_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    balance: float = Field(default=0.0)

class Customer(BaseModel):
    id: str = Field(default_factory=lambda _: uuid4().hex)
    name: str = Field(min_length=3)
    surname: str = Field(min_length=3)