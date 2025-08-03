from django.db import models


class Hero(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='heroes/')
    cta_text = models.CharField(max_length=100, blank=True, null=True)
    cta_link = models.URLField(blank=True, null=True)
    overlay_color = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
