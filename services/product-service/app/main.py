from fastapi import FastAPI
from app.metrics import setup_metrics
from app.api.products import router as products_router

app = FastAPI(title="Product Service", version="1.0.0", description="Product catalog (MongoDB)")

setup_metrics(app)
app.include_router(products_router, prefix="/products", tags=["products"])
