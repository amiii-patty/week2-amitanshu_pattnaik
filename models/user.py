from sqlalchemy import Column , Integer,String 
from sqlalchemy.orm import relationship
from db.base import Base


class Users(Base):
    __tablename__="users"
    
    user_id=Column(Integer,primary_key=True,index=True)
    name =Column(String, nullable=False)
    email = Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    mobile=Column(String)

    #one user can have many cart items.
    cart_items = relationship("Cart", back_populates="user")

    #one user can have many orders
    orders = relationship("Order", back_populates="user")