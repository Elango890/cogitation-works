from django.urls import path
from . import views
from .views import download_invoice

app_name = "orders"

urlpatterns = [
    path("place/<int:product_id>/", views.place_order, name="place_order"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("invoice/<int:order_id>/", views.invoice, name="invoice"),
    path("cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("checkout/", views.checkout, name="checkout"),

    path("invoice/pdf/<int:order_id>/", views.download_invoice, name="download_invoice"),

#path("invoice/pdf/<int:order_id>/", views.download_invoice, name="download_invoice")
#path('invoice/pdf/<int:order_id>/', download_invoice, name='invoice_pdf'),
]
