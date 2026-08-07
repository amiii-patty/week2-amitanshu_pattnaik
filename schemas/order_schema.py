from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Literal

class CheckoutRequest(BaseModel):
    user_id: int
    payment_method: Literal["cash", "upi"] 


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    order_date: datetime
    payment_method: str
    total_amount: float


class OrderDetailItem(BaseModel):
    details_id: int
    product_id: int
    product_name: str
    quantity: int
    price: float
    subtotal: float


class OrderDetailResponse(BaseModel):
    order_id: int
    user_id: int
    order_date: datetime
    payment_method: str
    total_amount: float
    items: List[OrderDetailItem]

