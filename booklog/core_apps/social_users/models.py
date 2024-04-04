from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class Admin(AbstractUser):
    class Meta:
        db_table = _("admin")
        verbose_name = _("Admin")
        verbose_name_plural = _("Admin")


class SocialUser(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.CharField(max_length=100, unique=True, editable=False,
                            verbose_name=_("Social user identifier"))
    name = models.CharField(max_length=50, editable=False,
                            verbose_name=_("Social user name"))
    provider = models.CharField(max_length=50, editable=False,
                                verbose_name=_("Social provider"))
    last_login = models.DateTimeField(verbose_name=_("last login"), auto_now=True)
    date_joined = models.DateTimeField(verbose_name=_("date joined"), auto_now_add=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.name
