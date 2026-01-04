from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationOut(BaseModel):
    id: int
    event_type: str
    order_id: Optional[int] = None
    user_email: Optional[str] = None
    channel: str
    subject: Optional[str] = None
    message: Optional[str] = None
    status: str
    error: Optional[str] = None
    payload_json: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True