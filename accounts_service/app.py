from fastapi import FastAPI
from routes import router as accounts_router

app = FastAPI(title="Accounts Service")

app.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
