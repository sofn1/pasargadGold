from django.db import models
from products.models.brand import Brand


class Product(models.Model):
    name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)
    category_id = models.CharField(max_length=64)  # MongoDB category ID as string

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    featured = models.BooleanField(default=False)  # ✅ NEW FIELD

    owner_name = models.CharField(max_length=255)
    owner_profile = models.URLField()

    short_description = models.TextField()
    description = models.TextField()

    features = models.JSONField(default=dict)  # {featureName: featureDesc}

    view_image = models.ImageField(upload_to="product/views/")
    images = models.JSONField(default=list)  # list of up to 5 image URLs or paths

    rel_news = models.JSONField(default=list, blank=True)  # list of news IDs
    rel_blogs = models.JSONField(default=list, blank=True)
    rel_products = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # Inside Product model
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    is_active = models.BooleanField(default=True)  # ✅ Add this line

    def __str__(self):
        return self.name
