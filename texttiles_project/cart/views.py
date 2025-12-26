from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import CartItem
from orders.models import Order, OrderItem


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, "Out of stock")
        return redirect("products:product_list")

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1}
    )

    if not created:
        if cart_item.quantity + 1 > product.stock:
            messages.error(request, "Stock limit reached")
        else:
            cart_item.quantity += 1
            cart_item.save()

    messages.success(request, "Added to cart")
    return redirect("cart:view_cart")


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total": total
    })


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    qty = int(request.POST.get("quantity", 1))

    if qty <= 0:
        item.delete()
    elif qty > item.product.stock:
        messages.error(request, "Stock exceeded")
    else:
        item.quantity = qty
        item.save()

    return redirect("cart:view_cart")


@login_required
def remove_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect("cart:view_cart")
