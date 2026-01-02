import boto3
from django.conf import settings

def list_s3_images(prefix="products/"):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    response = s3.list_objects_v2(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Prefix=prefix
    )

    images = []
    for obj in response.get("Contents", []):
        key = obj["Key"]
        if key.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            images.append((key, key))

    return images
