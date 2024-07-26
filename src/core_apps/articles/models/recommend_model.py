from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.shared.models import TimeStampedModel


class Recommend(TimeStampedModel):
    user = models.ForeignKey("social_users.SocialUser", on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="article_recommends")

    class Meta:
        verbose_name = _("Recommendation")
        verbose_name_plural = _("Recommendations")
        unique_together = ["user", "article"]
        ordering = ["-created_at"]
        db_table = "recommend"

    def __str__(self):
        return f"{self.user.username} recommends {self.article.title}"
