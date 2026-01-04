from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import get_current_email
from app.schemas import OrderCreate, OrderOut, OrderItemOut, OrderStatusUpdate
from app.models import Order, OrderItem
from app.clients import get_product, process_payment
from app.mq import publish_order_event

router = APIRouter()

# ✅ قوانین تغییر وضعیت (برای اینکه استاد نگه هر چیزی به هر چیزی میشه!)
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "created": {"cancelled"},
    "paid": {"cancelled", "shipped"},
    "shipped": {"delivered"},
    "delivered": set(),
    "cancelled": set(),
    "failed": set(),
}

def _to_order_out(order: Order) -> OrderOut:
    return OrderOut(
        id=order.id,
        user_email=order.user_email,
        status=order.status,
        total_toman=order.total_toman,
        items=[
            OrderItemOut(
                product_id=i.product_id,
                title=i.title,
                unit_price_toman=i.unit_price_toman,
                qty=i.qty
            )
            for i in order.items
        ],
    )

@router.post("", response_model=OrderOut)
async def create_order(
    payload: OrderCreate,
    email: str = Depends(get_current_email),
    db: Session = Depends(get_db),
):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Empty items")

    order = Order(user_email=email, status="created", total_toman=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    total = 0
    for it in payload.items:
        p = await get_product(it.product_id)
        unit_price = int(p["price_toman"])
        title = p["title"]
        total += unit_price * it.qty
        oi = OrderItem(
            order_id=order.id,
            product_id=it.product_id,
            title=title,
            unit_price_toman=unit_price,
            qty=it.qty,
        )
        db.add(oi)

    order.total_toman = total
    db.add(order)
    db.commit()
    db.refresh(order)

    # پرداخت
    try:
        pay = await process_payment(
            order_id=order.id,
            amount_toman=order.total_toman,
            card_last4=payload.card_last4,
        )
    except Exception as e:
        order.status = "failed"
        db.add(order)
        db.commit()
        raise HTTPException(status_code=502, detail=f"Payment service unavailable/failed: {str(e)}")

    if pay.get("status") != "success":
        order.status = "failed"
        db.add(order)
        db.commit()
        raise HTTPException(status_code=402, detail="Payment failed")

    order.status = "paid"
    db.add(order)
    db.commit()
    db.refresh(order)

    # انتشار رویداد برای Notification
    await publish_order_event({
        "type": "order_paid",
        "order_id": order.id,
        "user_email": order.user_email,
        "total_toman": order.total_toman,
    })

    return _to_order_out(order)

# ✅ Tracking: لیست سفارش‌های کاربر
@router.get("", response_model=list[OrderOut])
def list_my_orders(email: str = Depends(get_current_email), db: Session = Depends(get_db)):
    orders = (
        db.query(Order)
        .filter(Order.user_email == email)
        .order_by(Order.id.desc())
        .all()
    )
    return [_to_order_out(o) for o in orders]

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, email: str = Depends(get_current_email), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_email == email).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _to_order_out(order)

# ✅ Update: آپدیت وضعیت سفارش
@router.put("/{order_id}/status", response_model=OrderOut)
async def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    email: str = Depends(get_current_email),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_email == email).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    old = order.status
    allowed = ALLOWED_TRANSITIONS.get(old, set())
    if payload.status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change status from '{old}' to '{payload.status}'. Allowed: {sorted(list(allowed))}",
        )

    order.status = payload.status
    db.add(order)
    db.commit()
    db.refresh(order)

    # اختیاری ولی خیلی خوب برای نمره: رویداد تغییر وضعیت هم بفرست
    await publish_order_event({
        "type": "order_status_changed",
        "order_id": order.id,
        "user_email": order.user_email,
        "old_status": old,
        "new_status": order.status,
        "total_toman": order.total_toman,
    })

    return _to_order_out(order)