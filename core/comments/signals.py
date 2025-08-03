from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment


@receiver(post_save, sender=Comment)
def notify_on_reply(sender, instance, created, **kwargs):
    if created and instance.parent:
        parent_author = instance.parent.user
        print(f"📣 Notify {parent_author.phone_number}: Someone replied to your comment.")
        # You can later replace this with actual push/email/notification logic
