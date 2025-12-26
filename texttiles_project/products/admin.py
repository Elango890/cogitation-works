from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "get_category_name", "price", "stock")
    list_filter = ("category", "color", "size")
    search_fields = ("product_name",)

    # This method allows displaying category name in list_display
    def get_category_name(self, obj):
        return obj.category.category_name
    get_category_name.short_description = "Category"
