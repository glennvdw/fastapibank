from typing import Annotated, List, Optional

from fastapi import Depends, APIRouter, HTTPException, Query

from schemas import CreateTransactionRequest, TransactionResponse
from services.services import TransactionService
from dependencies import get_transaction_service
from exceptions import AccountNotFound

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)],
    payload: CreateTransactionRequest,
    ):
    try:
        transaction = transaction_service.create_transaction(payload)
    except AccountNotFound:
        raise HTTPException(status_code=422, detail="Unknown account id")

    return transaction


@router.get("/", response_model=List[TransactionResponse])
def list_transactions(
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)],
    account_id: str = Query(None, description="Filter by account ID"),
):
    return transaction_service.list_transactions(account_id=account_id)
