from pydantic import BaseModel, Field
from typing import List

class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)

class CartItemResponse(BaseModel):
    cart_id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartSummaryItem(BaseModel):
    cart_id: int
    product_id: int
    product_name: str
    unit_price: float
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True

class CartSummaryResponse(BaseModel):
    user_id: int
    items: List[CartSummaryItem]
    total_price: float