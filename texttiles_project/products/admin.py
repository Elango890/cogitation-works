from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

from .models import Category, Product
from .forms import ProductAdminForm   # make sure this exists

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

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
    readonly_fields = ("image_preview",)

    def get_category_name(self, obj):
        return obj.category.category_name
    get_category_name.short_description = "Category"

    def image_preview(self, obj):
        if obj.image_key:
            url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{obj.image_key}"
            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;" />',
                url
            )
        return "No Image Selected"

    image_preview.short_description = "Image Preview"
