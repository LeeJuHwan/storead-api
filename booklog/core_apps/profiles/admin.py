from django.contrib import admin

from .models import Profile


@admin.action(description="선택된 프로필 삭제")
def delete_profile_without_user(modeladmin, request, queryset):
    for profile in queryset:
        profile.delete()


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "pkid",
        "id",
        "user_name",
        "user",
    ]
    list_display_links = ["pkid", "id", "user", "user_name"]
    list_filter = ["id", "pkid"]
    actions = [delete_profile_without_user]

    def user_name(self, obj):
        return obj.user.username


admin.site.register(Profile, ProfileAdmin)
