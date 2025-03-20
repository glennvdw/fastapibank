from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

class TransactionType(str, Enum):
    # Currently only deposit from external accounts supported
    DEPOSIT = "deposit"


class Transaction(BaseModel):
    id: str = Field(default_factory=lambda _: uuid4().hex)
    amount: float = Field(gt=0, description="Amount of the transaction")
    message: str
    type: TransactionType
    timestamp: datetime = Field(description="Timestamp of the transaction")
    message: Optional[str] = Field(None, description="Optional message of the transaction")
    account_id: str
    counterparty_iban: str
