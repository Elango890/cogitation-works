from django import forms
from .models import Product
from products.utils import get_s3_images

class ProductS3ImageAdminForm(forms.ModelForm):

    s3_image_key = forms.ChoiceField(
        choices=[],
        required=False,
        label="Product Image (S3)"
    )

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        images = get_s3_images(prefix="products/")
        self.fields["s3_image_key"].choices = [
            ("", "---- Select Image from S3 ----")
        ] + [(img, img) for img in images]
