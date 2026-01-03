from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = [
            "id", "product_name", "category",
            "price", "discount", "description",
            "size", "color", "material",
            "stock", "s3_image_key",
        ]
