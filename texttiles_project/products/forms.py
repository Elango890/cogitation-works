from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "address", "quantity"]

from django import forms
from .models import Product
from .utils.s3 import list_s3_images

class ProductAdminForm(forms.ModelForm):
    image_key = forms.ChoiceField(
        choices=[],
        required=False,
        label="Select Image from S3"
    )

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image_key"].choices = list_s3_images()