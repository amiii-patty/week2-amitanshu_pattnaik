from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.base import get_db
from schemas import order_schema
from services import order_service

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/checkout", response_model=order_schema.OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(request: order_schema.CheckoutRequest, db: Session = Depends(get_db)):
    order = order_service.checkout(db, request)
    if not order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")
    return order


@router.get("/details/{order_id}", response_model=order_schema.OrderDetailResponse)
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    order = order_service.get_order_details(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.get("/{user_id}", response_model=list[order_schema.OrderResponse])
def get_order_history(user_id: int, db: Session = Depends(get_db)):
    return order_service.get_order_history(db, user_id)