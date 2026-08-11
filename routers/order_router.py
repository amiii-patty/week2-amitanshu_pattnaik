from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from db.base import get_db
from schemas import order_schema
from services import order_service

# Fix: removed HTTPException import — all error handling moved to service layer
router = APIRouter(prefix="/api/orders", tags=["Orders"])


# Fix: changed "/checkout" to "/" — POST method is self-describing, verb not needed in path
@router.post("/", response_model=order_schema.OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(request: order_schema.CheckoutRequest, db: Session = Depends(get_db)):
    return order_service.checkout(db, request)


# Fix: changed "/details/{order_id}" to "/{order_id}" — verb removed from path
# Fix: removed inline HTTPException — 404 guard is now in the service layer
@router.get("/{order_id}/details", response_model=order_schema.OrderDetailResponse)
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order_details(db, order_id)


# Fix: changed list[...] to List[...] for broader Python version compatibility
@router.get("/history/{user_id}", response_model=List[order_schema.OrderResponse])
def get_order_history(user_id: int, db: Session = Depends(get_db)):
    return order_service.get_order_history(db, user_id)