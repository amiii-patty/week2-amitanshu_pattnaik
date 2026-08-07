from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base

class Product(Base):
    __tablename__="product"

    product_id = Column(Integer,primary_key=True,index=True)
    product_name = Column(String,unique=True,nullable=False)
    description = Column(String,nullable=False)
    price = Column(Float,nullable=False)
    quantity = Column(Integer,nullable=False)
    url = Column(String)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)

    # Many products have one category
    category = relationship("Category", back_populates="products")

    # One product has many cart items
    cart_items = relationship("Cart", back_populates="product")

    # One product has many order detail rows
    order_details = relationship("OrderDetails", back_populates="product")