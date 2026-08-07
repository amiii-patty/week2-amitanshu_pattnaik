
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.base import get_db
from schemas import cart_schema
from services import cart_service

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.post("/add", response_model=cart_schema.CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_item(request: cart_schema.CartItemAdd, db: Session = Depends(get_db)):
    return cart_service.add_item(db, request)


@router.get("/{user_id}/summary", response_model=cart_schema.CartSummaryResponse)
def get_cart_summary(user_id: int, db: Session = Depends(get_db)):
    return cart_service.get_cart_summary(db, user_id)


@router.get("/{user_id}", response_model=list[cart_schema.CartItemResponse])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return cart_service.get_cart(db, user_id)


@router.put("/update/{cart_item_id}", response_model=cart_schema.CartItemResponse)
def update_item(cart_item_id: int, request: cart_schema.CartItemUpdate, db: Session = Depends(get_db)):
    item = cart_service.update_item(db, cart_item_id, request)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    return item


@router.delete("/remove/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(cart_item_id: int, db: Session = Depends(get_db)):
    item = cart_service.remove_item(db, cart_item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")