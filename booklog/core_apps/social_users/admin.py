from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm, SocialUserCreationForm
from .models import SocialUser


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    ordering = ["-date_joined"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = [
        "id",
        "username",
        "is_staff",
        "is_active",
    ]

    list_display_links = ["id", "username"]

    list_filter = [
        "username",
        "is_staff",
        "is_active",
    ]

    fieldsets = (
        (_("Login Credentials"), {"fields": ("username", "password")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    search_fields = ["username",]


class SocialAccount(admin.ModelAdmin):
    ordering = ["-date_joined"]
    form = UserChangeForm
    add_form = SocialUserCreationForm
    model = SocialUser

    list_display = [
        "pkid",
        "uuid",
        "provider",
        "name",
        "last_login",
        "date_joined",
    ]

    list_display_links = ["pkid", "name", "provider"]

    list_filter = [
        "name",
        "uuid",
        "provider",
        "last_login",
        "date_joined",
    ]

    search_fields = ["name", "provider"]


admin.site.register(User, UserAdmin)
admin.site.register(SocialUser, SocialAccount)
