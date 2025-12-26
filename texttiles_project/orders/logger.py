import logging
logger = logging.getLogger("orders")


def log_order_action(user, order, action):
    logger.info(
        f"ORDER {action} | User: {user.username} | "
        f"Order ID: {order.id} | Amount: {order.total_amount}"
    )
