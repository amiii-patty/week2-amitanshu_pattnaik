from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base import Base

class Order(Base):
    __tablename__ = "orders" 

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    order_date = Column(DateTime, server_default=func.now())  # auto-set on creation
    payment_method = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)

    # Many orders can have one user
    user = relationship("Users", back_populates="orders")

    # One order can have many order details
    order_details = relationship("OrderDetails", back_populates="order")