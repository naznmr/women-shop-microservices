from pydantic import BaseModel, Field

class PaymentRequest(BaseModel):
    order_id: str = Field(min_length=1, max_length=64)
    amount_toman: int = Field(ge=0)
    # فیلدهای کارت/درگاه در دنیای واقعی اینجا می‌آید؛ برای شبیه‌سازی ساده نگه داشتیم
    card_last4: str = Field(min_length=4, max_length=4, description="چهار رقم آخر کارت (شبیه‌سازی)")

class PaymentResponse(BaseModel):
    order_id: str
    amount_toman: int
    status: str
    message: str
