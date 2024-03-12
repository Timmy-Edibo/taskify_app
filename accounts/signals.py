from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def update_profile(sender, instance, created, **kwargs):
    """
    Signal to update profile completion status on creating new user.
    """
    if created:
        instance.updated_profile = all(
            getattr(instance, field, None) not in [None, ""]
            for field in ["client", "branch"]
        )
        instance.save()
