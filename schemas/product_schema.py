from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    product_name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    url: str = Field(min_length=1)
    category_id: int


# Fix: added dedicated schema for quantity update — avoids exposing unrelated fields
class ProductUpdateQuantity(BaseModel):
    quantity: int = Field(ge=0, description="New stock quantity, must be 0 or greater")


class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    description: str
    price: float
    quantity: int
    url: str
    category_id: int
    category_name: str

    class Config:
        from_attributes = True