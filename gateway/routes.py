from typing import Annotated, List, Optional
from os import getenv

from fastapi import APIRouter, HTTPException, Query
import requests
from schema import *

accounts_router = APIRouter()
transactions_router = APIRouter()

ACCOUNTS_SERVICE_URL = getenv("ACCOUNTS_SERVICE_URL", "http://localhost:8001")
TRANSACTIONS_SERVICE_URL = getenv("TRANSACTIONS_SERVICE_URL", "http://localhost:8002")


# @router.post("/", response_model=AccountResponse)
# def create_account():
#     try:
#         account = accounts_service.create_account(payload)
#     except CustomerNotFound:
#         raise HTTPException(status_code=422, detail="Unknown customer id")

#     return account


@accounts_router.get("/", response_model=List[AccountResponse])
def list_accounts(
    customer_id: str = Query(None, description="Filter by customer ID"),
):
    params = {}
    if customer_id:
        params["customer_id"] = customer_id
    
    try:
        resp = requests.get(f"{ACCOUNTS_SERVICE_URL}/accounts", params=params)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))


@accounts_router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: str, 
):
    try:
        resp = requests.get(f"{ACCOUNTS_SERVICE_URL}/accounts/{account_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

@transactions_router.post("/", response_model=TransactionResponse)
def create_transaction(
    payload: CreateTransactionRequest,
    ):
    try:
        resp = requests.post(f"{TRANSACTIONS_SERVICE_URL}/transactions", json=payload.dict())
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))


@transactions_router.get("/", response_model=List[TransactionResponse])
def list_transactions(
    account_id: str = Query(None, description="Filter by account ID"),
):
    try:
        filter = f"?account_id={account_id}" if account_id else ""
        resp = requests.get(f"{TRANSACTIONS_SERVICE_URL}/transactions/{filter}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))
