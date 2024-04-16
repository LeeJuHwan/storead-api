import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from core_apps.profiles.models import Profile
from core_apps.social_users.models import SocialUser

logger = logging.getLogger(__name__)


@receiver(post_save, sender=SocialUser)
def create_user_profile(sender, instance, created, **kwagrs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"[profile signal] {instance}'s profile has been created.")
