from fastapi import FastAPI
from app.metrics import setup_metrics
from app.db import init_db
from app.api.auth import router as auth_router
from app.api.users import router as users_router

app = FastAPI(title="User Service", version="1.0.0", description="User management + JWT auth")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()

setup_metrics(app)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
