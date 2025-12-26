from django.urls import path
from . import views
from .views import product_list 

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product_list"),  
    
]
