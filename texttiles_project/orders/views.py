import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from weasyprint import HTML
from cart.models import CartItem
from .utils import send_order_success_email
from .models import Order, OrderItem
from products.models import Product
from django.http import HttpResponse
from django.template.loader import render_to_string
import logging
#from weasyprint import HTML
logger = logging.getLogger("orders")

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        mobile_number = request.POST.get("mobile_number")
        address = request.POST.get("address")
        quantity = int(request.POST.get("quantity", 1))

        if quantity <= 0:
            logger.warning(
                f"INVALID QUANTITY | User={request.user} | Product={product.id}"
            )
            messages.error(request, "Invalid quantity")
            return redirect("products:product_list")

        if quantity > product.stock:
            logger.warning(
                f"INSUFFICIENT STOCK | User={request.user} | "
                f"Product={product.id} | Requested={quantity} | Available={product.stock}"
            )
            messages.error(request, "Insufficient stock")
            return redirect("products:product_list")

        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            mobile_number=mobile_number,
            address=address,
            status=Order.PLACED
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        product.stock -= quantity
        product.save()

        # ✅ MAIN LOG ENTRY
        logger.info(
            f"ORDER PLACED | "
            f"OrderID={order.id} | "
            f"User={request.user.username} | "
            f"Product={product.product_name} | "
            f"Qty={quantity} | "
            f"Total={product.price * quantity}"
        )

        send_order_success_email(request.user, order)
        messages.success(request, "✅ Order placed successfully")
        return redirect("orders:order_success", order_id=order.id)

    return render(request, "orders/order_form.html", {"product": product})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == Order.PLACED:
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        order.status = Order.CANCELLED
        order.save()

        logger.info(
            f"ORDER CANCELLED | OrderID={order.id} | User={request.user.username}"
        )

        messages.success(request, "❌ Order cancelled successfully")

    return redirect("orders:my_orders")


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        logger.warning(f"EMPTY CART CHECKOUT | User={request.user.username}")
        messages.error(request, "Cart is empty")
        return redirect("products:product_list")

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        mobile_number = request.POST.get("mobile_number")
        address = request.POST.get("address")

        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            mobile_number=mobile_number,
            address=address,
            status=Order.PLACED
        )

        total_items = 0

        for item in cart_items:
            if item.quantity > item.product.stock:
                logger.error(
                    f"CHECKOUT FAILED | OrderID={order.id} | "
                    f"Product={item.product.product_name}"
                )
                messages.error(
                    request,
                    f"Insufficient stock for {item.product.product_name}"
                )
                order.delete()
                return redirect("cart:view_cart")

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save()
            total_items += item.quantity

        cart_items.delete()

        logger.info(
            f"CART CHECKOUT SUCCESS | OrderID={order.id} | "
            f"User={request.user.username} | Items={total_items}"
        )

        send_order_success_email(request.user, order)
        messages.success(request, "✅ Order placed successfully")
        return redirect("orders:order_success", order_id=order.id)

    return render(request, "cart/checkout.html", {"cart_items": cart_items})


@login_required
def invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/invoice.html", {"order": order})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order_success.html", {"order": order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})


#@login_required
#def download_invoice(request, order_id):
#    # Get the order for the logged-in user
#    order = get_object_or_404(Order, id=order_id, user=request.user)
#    
#    # Render HTML template with order data
#    html_string = render_to_string('orders/invoice_pdf.html', {'order': order})
#    
#    # Create HTTP response with PDF content
#    response = HttpResponse(content_type='application/pdf')
#    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
#    
#    # Generate PDF
#    HTML(string=html_string).write_pdf(response)
#    
#    return response



def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Absolute path for logo (inside media/product/)
    logo_path = os.path.join(settings.MEDIA_ROOT, 'products/logo.jpg')
    logo_path = f'file://{logo_path}'

    # Absolute paths for product images
    for item in order.items.all():
        item.product_image_path = f'file://{os.path.join(settings.MEDIA_ROOT, item.product.image.name)}'

    html_string = render_to_string(
        'orders/invoice_pdf.html',
        {
            'order': order,
            'logo_path': logo_path,
        }
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    HTML(string=html_string).write_pdf(response)
    return response
