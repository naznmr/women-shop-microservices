from fastapi import FastAPI
from app.metrics import setup_metrics
from app.db import init_db
from app.api import router as payment_router

app = FastAPI(title="Payment Service", version="1.0.0", description="Simulated payment processing")

@app.on_event("startup")
def _startup():
    init_db()

setup_metrics(app)
app.include_router(payment_router, prefix="/payments", tags=["payments"])
