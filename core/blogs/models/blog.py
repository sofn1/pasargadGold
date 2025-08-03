from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)
    category_id = models.CharField(max_length=64)  # MongoDB category ID

    writer_name = models.CharField(max_length=255)
    writer_profile = models.URLField()

    publish_time = models.DateTimeField()
    read_time = models.PositiveIntegerField()

    short_description = models.TextField()
    content = models.TextField()

    view_image = models.ImageField(upload_to="blogs/view/")
    rel_news = models.JSONField(default=list, blank=True)
    rel_blogs = models.JSONField(default=list, blank=True)
    rel_products = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
