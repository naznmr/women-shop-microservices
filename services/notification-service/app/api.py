from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Notification
from app.schemas import NotificationOut

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/latest", response_model=list[NotificationOut])
def latest(limit: int = 20, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 100))
    rows = db.query(Notification).order_by(Notification.id.desc()).limit(limit).all()
    return rows

@router.get("/{notification_id}", response_model=NotificationOut)
def get_one(notification_id: int, db: Session = Depends(get_db)):
    row = db.query(Notification).filter(Notification.id == notification_id).first()
    return row