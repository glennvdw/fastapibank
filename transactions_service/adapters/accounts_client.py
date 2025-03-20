import os
import requests
from typing import Optional
from ports.accounts_port import IAccountsPort
from schemas import AccountResponse
from settings import ACCOUNTS_SERVICE_URL
from datetime import datetime

class AccountsClient(IAccountsPort):
    """Concrete adapter to call the Accounts microservice via HTTP."""

    def get_account(self, account_id: str) -> Optional[AccountResponse]:
        url = f"{ACCOUNTS_SERVICE_URL}/accounts/{account_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return AccountResponse(**data)
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()

    def update_balance(
        self, 
        account_id: str, 
        new_balance: float,
        timestamp: datetime,
    ):
        url = f"{ACCOUNTS_SERVICE_URL}/accounts/{account_id}/balance"
        response = requests.patch(
            url, 
            json={'new_balance': new_balance, 'timestamp': timestamp.isoformat()}
        )
        response.raise_for_status()
