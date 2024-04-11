from django.contrib import admin

from . import models


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pkid", "author", "title", "slug", "view_count", "view_recommends", "estimated_reading_time"]
    list_display_links = ["pkid", "author"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title", "body", "tags"]
    orderfing = ["-created_at"]


class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ["pkid", "article", "user", "viewer_ip"]
    list_display_links = ["pkid", "article"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user", "viewer_ip"]


class RecommendAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "article"]
    list_display_links = ["id", "user"]
    list_filter = ["created_at", "updated_at"]


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleView, ArticleViewAdmin)
admin.site.register(models.Recommend, RecommendAdmin)
