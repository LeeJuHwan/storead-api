from core_apps.common.models import TimeStampedModel
from core_apps.social_users.models import SocialUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(TimeStampedModel):
    user = models.OneToOneField(SocialUser, on_delete=models.CASCADE, related_name="profile")
    about_me = models.TextField(verbose_name=_("about me"), default=_("say something about yourself"))
    profile_photo = models.ImageField(verbose_name=_("profile photo"), upload_to="profile_photo", null=True)
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,  # NOTE: Follow asymmetric relationships, not each other
        related_name="following",
        blank=True,
    )

    class Meta:
        db_table = "profiles"
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return f"{self.user.username}'s Profile" if self.user.username else "Unkown's Profile"

    def follow(self, profile):
        self.followers.add(profile)

    def unfollow(self, profile):
        self.followers.remove(profile)

    def is_following(self, profile):
        return self.followers.filter(pkid=profile.pkid).exists()
