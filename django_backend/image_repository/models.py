from django.db import models
from cloudinary.models import CloudinaryField
import uuid
from django.conf import settings

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_imaages"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner_images"
    )
    image = CloudinaryField("stock_images")
    description = models.CharField(
        max_length=500,
        help_text="Image description e.g requirements to get to this level",
    )
    price = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Sales(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller"
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buyer"
    )
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="image_sales")
    bought_on = models.DateTimeField(auto_now_add=True)