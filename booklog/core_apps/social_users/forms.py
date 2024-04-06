from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model

from .models import SocialUser

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ["username"]

    error_messages = {
        "username": "A user with this username already exists.",
    }


class SocialUserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = SocialUser
        fields = ["uuid", "name", "provider"]

    error_messages = {
        "name": "A user with this username already exists.",
    }
