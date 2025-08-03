from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from accounts.models import User

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    edited = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='visible', choices=[
        ('visible', 'Visible'),
        ('hidden', 'Hidden'),
        ('flagged', 'Flagged')
    ])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.phone_number} → {self.content[:30]}'

    class Meta:
        ordering = ['created_at']


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="like_entries")

    class Meta:
        unique_together = ['user', 'comment']
