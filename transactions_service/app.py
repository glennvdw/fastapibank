from fastapi import FastAPI
from routes import router as transactions_router

app = FastAPI(title="Transactions Service")

app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
