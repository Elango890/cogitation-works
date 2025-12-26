import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger("email")


def send_order_success_email(user, order):
    """
    Sends order confirmation email (TEXT + HTML) to customer
    """

    customer_name = (
        user.get_full_name()
        if user.get_full_name()
        else user.username
    )

    subject = f"Order Confirmation – Order #{order.id}"

    # ---------------- TEXT EMAIL (Fallback) ----------------
    text_message = f"""
Hi {customer_name},

Thank you for your order!

Order ID: {order.id}
Order Date: {order.created_at.strftime('%d %b %Y')}
Total Amount: ₹{order.total_amount()}

We appreciate your business.

Regards,
TextTiles Team
"""

    # ---------------- BUILD ORDER ITEMS TABLE ----------------
    rows = ""
    for item in order.items.all():
        rows += f"""
        <tr>
            <td>{item.product.product_name}</td>
            <td align="center">{item.quantity}</td>
            <td align="right">₹{item.price}</td>
            <td align="right">₹{item.total_price()}</td>
        </tr>
        """

    # ---------------- HTML EMAIL ----------------
    html_message = f"""
    <html>
    <body style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#333;">

        <p>Hi <strong>{customer_name}</strong>,</p>

        <p>
            Thank you for placing your order with <strong>TextTiles</strong>.
            We’re pleased to confirm that your order has been received.
        </p>

        <p>
            <strong>Order ID:</strong> {order.id}<br>
            <strong>Order Date:</strong> {order.created_at.strftime('%d %b %Y')}<br>
            <strong>Total Amount:</strong> ₹{order.total_amount()}
        </p>

        <h4>Order Summary</h4>

        <table width="100%" border="1" cellspacing="0" cellpadding="6"
               style="border-collapse:collapse;">
            <thead>
                <tr>
                    <th align="left">Product</th>
                    <th align="center">Quantity</th>
                    <th align="right">Price</th>
                    <th align="right">Total</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <p style="margin-top:15px;">
            We’ll notify you once your order is shipped.
        </p>

        <p>
            Regards,<br>
            <strong>TextTiles Team</strong>
        </p>

        <p style="font-size:12px;color:#777;">
            This is an automated email. Please do not reply.
        </p>

    </body>
    </html>
    """

    # ---------------- SEND EMAIL ----------------
    try:
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(
            f"EMAIL SENT | User: {user.username} | Order ID: {order.id} | To: {user.email}"
        )

    except Exception as e:
        logger.error(
            f"EMAIL FAILED | User: {user.username} | Order ID: {order.id} | Error: {str(e)}"
        )
        raise
