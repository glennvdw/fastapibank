from fastapi import FastAPI
from routes import accounts_router, transactions_router

app = FastAPI(title="Bank")

app.include_router(accounts_router, prefix="/accounts")
app.include_router(transactions_router, prefix="/transactions")
