from django.db import models


class Banner(models.Model):
    POSITION_CHOICES = [
        ('top', 'Top'),
        ('middle', 'Middle'),
        ('bottom', 'Bottom'),
    ]

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    button_text = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"{self.title} - {self.position}"
