from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product
from products.product_admin_forms import ProductS3ImageAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductS3ImageAdminForm

    list_display = (
        "id",
        "product_name",
        "get_category_name",
        "price",
        "stock",
        "image_preview",
    )
    list_filter = ("category", "color", "size")
    search_fields = ("product_name",)

    def get_category_name(self, obj):
        return obj.category.category_name
    get_category_name.short_description = "Category"

    def image_preview(self, obj):
        if obj.image_url():
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                obj.image_url()
            )
        return "No Image"

    image_preview.short_description = "Image"
