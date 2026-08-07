from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    product_name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    url: str = Field(min_length=1)
    category_id: int

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