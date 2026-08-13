
from fastapi import FastAPI
from db.base import engine, Base
from routers import user_router, category_router, product_router, cart_router, order_router



#FastAPI app instance
app = FastAPI(docs_url='/shoppingapp',
              title = 'Online Shopping API',
              description = 'Welcome to this shopping website, we hope you find what you are looking for :)')

#register all the routers, so fastapi has idea that these endpoint exist.
app.include_router(user_router.router)
app.include_router(category_router.router)  
app.include_router(product_router.router)  
app.include_router(cart_router.router)
app.include_router(order_router.router)
