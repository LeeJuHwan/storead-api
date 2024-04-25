from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.articles.models import Article
from core_apps.common.models import TimeStampedModel

User = get_user_model()


class Comment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True
    )
    content = models.TextField(verbose_name=_("comment"))

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} commented on {self.article.title}"
