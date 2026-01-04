import random
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Payment
from app.schemas import PaymentRequest, PaymentResponse

router = APIRouter()

def should_fail(card_last4: str, fail_rate: float) -> bool:
    # قانون شبیه‌سازی: اگر رقم آخر فرد باشد احتمال خطا بیشتر
    base = fail_rate
    if int(card_last4[-1]) % 2 == 1:
        base = min(0.8, fail_rate + 0.2)
    return random.random() < base

@router.post("/process", response_model=PaymentResponse)
def process_payment(
    payload: PaymentRequest,
    fail_rate: float = Query(default=0.15, ge=0.0, le=1.0, description="نرخ خطا برای تست"),
    db: Session = Depends(get_db),
):
    failed = should_fail(payload.card_last4, fail_rate)
    status = "failed" if failed else "success"
    message = "پرداخت ناموفق (شبیه‌سازی)" if failed else "پرداخت موفق"
    p = Payment(order_id=payload.order_id, amount_toman=payload.amount_toman, status=status)
    db.add(p)
    db.commit()
    return PaymentResponse(order_id=payload.order_id, amount_toman=payload.amount_toman, status=status, message=message)
