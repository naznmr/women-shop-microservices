from fastapi import FastAPI
from app.metrics import setup_metrics
from app.db import init_db
from app.api.orders import router as orders_router

app = FastAPI(title="Order Service", version="1.0.0", description="Orders + sync payment + async notifications")

@app.on_event("startup")
def _startup():
    init_db()

setup_metrics(app)
app.include_router(orders_router, prefix="/orders", tags=["orders"])
