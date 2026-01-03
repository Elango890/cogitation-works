from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    product_name = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    size = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=100, blank=True)
    stock = models.PositiveIntegerField(default=0)

    # Existing upload (optional)
    #image = models.ImageField(upload_to="products/", null=True, blank=True)

    # ✅ NEW: S3 image key
    s3_image_key = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Select image from S3 bucket"
    )

    @property
    def discounted_price(self):
        return self.price - self.discount

    def image_url(self):
        if self.s3_image_key:
            return f"https://texttiles-product-images.s3.amazonaws.com/{self.s3_image_key}"
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.product_name
