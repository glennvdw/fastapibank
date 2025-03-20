from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CreateAccountRequest(BaseModel):
    customer_id: str = Field(min_length=1)
    name: str = Field(min_length=1)


class AccountResponse(BaseModel):
    id: str
    customer_id: str
    name: str
    balance: float

class TransactionType(str, Enum):
    DEPOSIT = "deposit"

class CreateTransactionRequest(BaseModel):
    account_id: str = Field(min_length=1)
    amount: float = Field(gt=0, description="Amount of the transaction")
    message: str
    type: TransactionType
    message: Optional[str] = Field(None, description="Optional message of the transaction")
    counterparty_iban: str
    account_id: str


class TransactionResponse(BaseModel):
    id: str
    amount: float
    message: str
    type: TransactionType
    timestamp: datetime = Field(description="Timestamp of the transaction")
    message: Optional[str] = Field(None, description="Optional message of the transaction")
    counterparty_iban: str
    account_id: str
