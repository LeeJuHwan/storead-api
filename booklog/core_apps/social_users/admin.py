from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.backends import BaseBackend
from django.utils.translation import gettext_lazy as _

from .forms import SocialUserCreationForm, UserChangeForm, UserCreationForm
from .models import Admin

User = get_user_model()


@admin.action(description="선택된 사용자 삭제")
def delete_user_and_profile(modeladmin, request, queryset):
    for user in queryset:
        user.delete()


class AdminAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            admin = Admin.objects.get(username=username)
            if admin.check_password(password):
                return admin
        except Admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None


class UserAdmin(BaseUserAdmin):
    ordering = ["-date_joined"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = Admin

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

    search_fields = [
        "username",
    ]
    actions = [delete_user_and_profile]


class SocialAccount(admin.ModelAdmin):
    ordering = ["-date_joined"]
    form = UserChangeForm
    add_form = SocialUserCreationForm
    model = User

    list_display = [
        "pkid",
        "uuid",
        "provider",
        "username",
        "last_login",
        "date_joined",
    ]

    list_display_links = ["pkid", "uuid", "username", "provider"]

    list_filter = [
        "username",
        "uuid",
        "provider",
        "last_login",
        "date_joined",
    ]

    search_fields = ["username", "provider"]
    actions = [delete_user_and_profile]


admin.site.register(Admin, UserAdmin)
admin.site.register(User, SocialAccount)
