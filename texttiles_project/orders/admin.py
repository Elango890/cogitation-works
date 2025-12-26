from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer_name",
        "mobile_number",
        "status",
        "created_at",
        "order_total",
    )

    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "mobile_number", "user__username")
    ordering = ("-created_at",)

    readonly_fields = ("created_at",)  # ✅ FIXED

    fieldsets = (
        ("Customer Info", {
            "fields": ("user", "customer_name", "mobile_number", "address")
        }),
        ("Order Status", {
            "fields": ("status",)
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )

    inlines = [OrderItemInline]

    def order_total(self, obj):
        return obj.total_amount()

    order_total.short_description = "Total Amount"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
