from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from .models import Product, Category

@login_required
def product_list(request):
    page_number = request.GET.get("page", 1)
    search = request.GET.get("search", "")
    category = request.GET.get("category", "")

    cache_key = f"products_{page_number}_{search}_{category}"
    page_obj = cache.get(cache_key)

    if not page_obj:
        products = Product.objects.all().select_related('category').only(
            "id", "product_name", "price", "discount", "size",
            "color", "material", "stock", "image", "category__category_name"
        ).order_by("id")

        if search:
            products = products.filter(product_name__icontains=search)
        if category:
            products = products.filter(category__id=category)

        paginator = Paginator(products, 20)  # 20 products per page
        page_obj = paginator.get_page(page_number)
        cache.set(cache_key, page_obj, 60 * 5)  # cache for 5 minutes

    categories = cache.get("all_categories")
    if not categories:
        categories = Category.objects.all()
        cache.set("all_categories", categories, 60 * 60)

    return render(
        request,
        "products/product_list.html",
        {"page_obj": page_obj, "categories": categories, "search": search, "selected_category": category}
    )
