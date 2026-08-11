from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from db.base import get_db
from schemas import cart_schema
from services import cart_service

# Fix: removed HTTPException import — 404 handling moved entirely to service layer
router = APIRouter(prefix="/api/cart", tags=["Cart"])


# Fix: changed "/add" to "/" — verb does not belong in the path, POST is self-describing
@router.post("/", response_model=cart_schema.CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_item(request: cart_schema.CartItemAdd, db: Session = Depends(get_db)):
    return cart_service.add_item(db, request)


# Fix: added List[] wrapper on response_model — list[...] lowercase is Python 3.9+ only, List is safer
@router.get("/{user_id}", response_model=List[cart_schema.CartItemResponse])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return cart_service.get_cart(db, user_id)


@router.get("/{user_id}/summary", response_model=cart_schema.CartSummaryResponse)
def get_cart_summary(user_id: int, db: Session = Depends(get_db)):
    return cart_service.get_cart_summary(db, user_id)


# Fix: changed PUT to PATCH — only quantity is being updated, not the full resource
# Fix: changed "/update/{cart_item_id}" to "/{cart_item_id}" — verb removed from path
# Fix: removed inline HTTPException — 404 guard is now in the service layer
@router.patch("/{cart_item_id}", response_model=cart_schema.CartItemResponse)
def update_item(cart_item_id: int, request: cart_schema.CartItemUpdate, db: Session = Depends(get_db)):
    return cart_service.update_item(db, cart_item_id, request)


# Fix: changed "/remove/{cart_item_id}" to "/{cart_item_id}" — verb removed from path
# Fix: removed inline HTTPException — 404 guard is now in the service layer
@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(cart_item_id: int, db: Session = Depends(get_db)):
    cart_service.remove_item(db, cart_item_id)