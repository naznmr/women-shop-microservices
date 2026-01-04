from pydantic import BaseModel, Field
from typing import Literal

Season = Literal["بهار", "تابستان", "پاییز", "زمستان"]

class ProductCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200, description="نام محصول")
    description: str = Field(default="", max_length=2000)
    category: str = Field(min_length=2, max_length=100, description="دسته‌بندی (مانتو، شومیز، ...)")
    season: Season
    price_toman: int = Field(ge=0, description="قیمت به تومان")
    sizes: list[str] = Field(default_factory=list, description="مثلاً: S/M/L/XL یا 36/38/40")
    colors: list[str] = Field(default_factory=list, description="مثلاً: مشکی، سفید، سرمه‌ای")
    stock: int = Field(ge=0, default=0)
    image_url: str | None = Field(default=None, description="URL عکس (اختیاری)")

class ProductOut(ProductCreate):
    id: str

class ProductUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    category: str | None = Field(default=None, min_length=2, max_length=100)
    season: Season | None = None
    price_toman: int | None = Field(default=None, ge=0)
    sizes: list[str] | None = None
    colors: list[str] | None = None
    stock: int | None = Field(default=None, ge=0)
    image_url: str | None = None
