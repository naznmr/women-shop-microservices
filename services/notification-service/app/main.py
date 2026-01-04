from fastapi import FastAPI
from app.metrics import setup_metrics
from app.api import router as api_router
from app.db import init_db

app = FastAPI(
    title="Notification Service",
    version="1.0.0",
    description="Consumes RabbitMQ events, sends email (SMTP/MailHog) and stores notifications in its own database."
)

setup_metrics(app)
app.include_router(api_router, prefix="/notifications", tags=["notifications"])

@app.on_event("startup")
def startup():
    init_db()