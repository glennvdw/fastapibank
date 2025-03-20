from typing import Annotated, List, Optional

from fastapi import Depends, APIRouter, HTTPException, Query

from schemas import CreateAccountRequest, AccountResponse, UpdateBalanceRequest
from services.services import AccountsService
from dependencies import get_accounts_service
from exceptions import CustomerNotFound, AccountNotFoundError

router = APIRouter()

@router.post("/", response_model=AccountResponse)
def create_account(
    accounts_service: Annotated[AccountsService, Depends(get_accounts_service)],
    payload: CreateAccountRequest,
    ):
    try:
        account = accounts_service.create_account(payload)
    except CustomerNotFound:
        raise HTTPException(status_code=422, detail="Unknown customer id")

    return account


@router.get("/", response_model=List[AccountResponse])
def list_accounts(
    accounts_service: Annotated[AccountsService, Depends(get_accounts_service)],
    customer_id: str = Query(None, description="Filter by customer ID"),
):
    """
    GET /accounts?customer_id=XYZ  -> returns accounts belonging to that customer
    GET /accounts                  -> returns all accounts
    """
    return accounts_service.list_accounts(customer_id=customer_id)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: str, 
    accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
):
    account = accounts_service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.patch("/{account_id}/balance", response_model=AccountResponse)
def update_balance_endpoint(
    account_id: str,
    payload: UpdateBalanceRequest,
    accounts_service: Annotated[AccountsService, Depends(get_accounts_service)],
):
    try:
        account = accounts_service.update_balance(
            account_id=account_id,
            new_balance=payload.new_balance,
            timestamp=payload.timestamp
        )
        return AccountResponse(**account.dict())
    except AccountNotFoundError:
        raise HTTPException(status_code=404, detail="Account not found")
