from django.db.models.signals import post_save
from django.dispatch import receiver

from core_apps.profiles.models import Profile
from config.settings.base import AUTH_USER_MODEL


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwagrs):
    if created:
        Profile.objects.create(user=instance)
