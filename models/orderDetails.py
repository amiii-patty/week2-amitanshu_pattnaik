from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class OrderDetails(Base):
    __tablename__ = "orderdetails"

    details_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Many order details have one order
    order = relationship("Order", back_populates="order_details")

    # Many order details can have one product
    product = relationship("Product", back_populates="order_details")