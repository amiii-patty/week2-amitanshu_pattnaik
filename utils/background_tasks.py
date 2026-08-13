from utils.logger import logger


def log_order_confirmation(order_id: int) -> None:
    logger.info(
        "Background task completed: order confirmation for order_id=%s",
        order_id,
    )