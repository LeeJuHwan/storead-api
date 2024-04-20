import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from core_apps.profiles.models import Profile
from config.settings.base import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwagrs):
    logger.info(f"created: {created}")
    if created:
        logger.info(f"instance: {instance}")
        Profile.objects.create(user=instance)
        logger.info(f"[profile signal] {instance}'s profile has been created.")
