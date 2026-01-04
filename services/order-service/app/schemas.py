from pydantic import BaseModel, Field
from typing import Literal

class OrderItemIn(BaseModel):
    product_id: str
    qty: int = Field(ge=1, le=20)

class OrderCreate(BaseModel):
    items: list[OrderItemIn]
    card_last4: str = Field(min_length=4, max_length=4)

# ✅ وضعیت‌های سفارش (برای OpenAPI هم خیلی تمیز درمیاد)
OrderStatus = Literal["created", "paid", "failed", "cancelled", "shipped", "delivered"]

# ✅ بدنه درخواست برای آپدیت وضعیت
class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderItemOut(BaseModel):
    product_id: str
    title: str
    unit_price_toman: int
    qty: int

class OrderOut(BaseModel):
    id: int
    user_email: str
    status: str
    total_toman: int
    items: list[OrderItemOut]