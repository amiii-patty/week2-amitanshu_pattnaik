from db.base import Base, engine
from models import cart, category, order, orderDetails, product, user 


Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")