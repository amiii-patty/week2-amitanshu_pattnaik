from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    category_name: str = Field(min_length=1, max_length=100)

class CategoryResponse(BaseModel):
    category_id: int
    category_name: str

    class Config:
        from_attributes = True
