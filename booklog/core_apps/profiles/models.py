from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.social_users.models import SocialUser
from core_apps.common.models import TimeStampedModel


class Profile(TimeStampedModel):
    user = models.OneToOneField(SocialUser, on_delete=models.CASCADE, related_name="profile")
    about_me = models.TextField(verbose_name=_("about me"), default=_("say something about yourself"))
    profile_photo = models.ImageField(verbose_name=_("profile photo"), upload_to="profile_photo")
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,  # NOTE: Follow asymmetric relationships, not each other
        related_name="following",
        blank=True,
    )

    def __str__(self):
        return f"{self.user.name}'s Profile"

    def follow(self, profile):
        self.followers.add(profile)

    def unfollow(self, profile):
        self.followers.remove(profile)

    def follower_list(self, profile):
        self.followers.all(profile)

    def is_following(self, profile):
        return self.followers.filter(pkid=profile.pkid).exists()
