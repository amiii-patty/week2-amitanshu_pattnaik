
from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session
from typing import List
from db.base import get_db
from schemas import order_schema
from services import order_service
from utils.jwt_handler import get_current_user, require_admin
from utils.logger import logger
from utils.background_tasks import log_order_confirmation



# Fix: removed HTTPException import — all error handling moved to service layer

router = APIRouter(prefix="/api", tags=["Orders"])

# Fix: changed "/checkout" to "/" — POST method is self-describing, verb not needed in path
@router.post(
    "/orders/",
    response_model=order_schema.OrderResponse,
    status_code=status.HTTP_201_CREATED,
)

def checkout(
    request: order_schema.CheckoutRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    logger.info("Checkout route started: POST /api/orders/")
    result = order_service.checkout(
        db,
        request,
        current_user,
    )
    background_tasks.add_task(
        log_order_confirmation,
        result["order_id"],
    )

    logger.info("Checkout route completed: POST /api/orders/")
    return result

# Fix: changed "/details/{order_id}" to "/{order_id}/details" — verb removed from path
# Fix: removed inline HTTPException — 404 guard is now in service layer

@router.get(

    "/orders/{order_id}/details",
    response_model=order_schema.OrderDetailResponse,
)

def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),

):
    logger.info("Order details route started: GET /api/orders/%s/details", order_id)
    result = order_service.get_order_details(
        db,
        order_id,
        current_user,
    )

    logger.info(
        "Order details route completed: GET /api/orders/%s/details",
        order_id,
    )
    return result



# Fix: changed list[...] to List[...] for broader Python version compatibility
@router.get(
    "/orders/history/{user_id}",
    response_model=List[order_schema.OrderResponse],
)

def get_order_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    logger.info(
        "Order history route started: GET /api/orders/history/%s",
        user_id,
    )

    result = order_service.get_order_history(
        db,
        user_id,
        current_user,
    )

    logger.info(
        "Order history route completed: GET /api/orders/history/%s",
        user_id,
    )
    return result

@router.get(
    "/admin/orders",
    response_model=List[order_schema.OrderResponse],
)
def get_all_orders(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    logger.info(
        "Admin orders route started: GET /api/admin/orders",
    )
    result = order_service.get_all_orders(db)
    logger.info(
        "Admin orders route completed: GET /api/admin/orders",
    )
    return result