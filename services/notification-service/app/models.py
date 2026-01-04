from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)
    order_id = Column(Integer, nullable=True)
    user_email = Column(String(255), nullable=True)

    channel = Column(String(20), nullable=False, default="email")   # email/sms
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=True)

    status = Column(String(20), nullable=False, default="stored")   # stored/sent/failed
    error = Column(Text, nullable=True)

    payload_json = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)