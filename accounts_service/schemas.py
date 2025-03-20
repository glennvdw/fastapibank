from typing import List
from pydantic import BaseModel, Field
from models import Account
from datetime import datetime

class CreateAccountRequest(BaseModel):
    """
    Request body when opening a new account for a given user.
    """
    customer_id: str = Field(min_length=1)
    name: str = Field(min_length=1)


class AccountResponse(BaseModel):
    id: str
    customer_id: str
    name: str
    balance: float


class UpdateBalanceRequest(BaseModel):
    new_balance: float
    timestamp: datetime