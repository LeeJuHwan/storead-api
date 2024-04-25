from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "pkid",
        "id",
        "user",
        "article",
        "parent_comment",
        "content",
        "created_at",
    ]
    list_display_links = ["pkid", "id", "user"]


admin.site.register(Comment, CommentAdmin)