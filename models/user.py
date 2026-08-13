from sqlalchemy import Column , Integer,String 
from sqlalchemy.orm import relationship
from db.base import Base


class Users(Base):
    __tablename__="users"
    
    user_id=Column(Integer,primary_key=True,index=True)
    name =Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    mobile=Column(String)

    role = Column(String, nullable=False, default="customer")

    #one user can have many cart items.
    cart_items = relationship("Cart", back_populates="user")

    #one user can have many orders
    orders = relationship("Order", back_populates="user")