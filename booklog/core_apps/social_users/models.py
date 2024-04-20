from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = Admin(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = Admin(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Admin(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'password']
    objects = CustomUserManager()

    class Meta:
        db_table = _("admin")
        verbose_name = _("Admin")
        verbose_name_plural = _("Admin")


class SocialUser(AbstractBaseUser):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.CharField(max_length=100, unique=True, verbose_name=_("Social user identifier"))
    username = models.CharField(max_length=50, unique=True, verbose_name=_("Social user name"))
    provider = models.CharField(max_length=50, verbose_name=_("Social provider"))
    last_login = models.DateTimeField(verbose_name=_("last login"), auto_now=True)
    date_joined = models.DateTimeField(verbose_name=_("date joined"), auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["uuid", "provider"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.uuid
