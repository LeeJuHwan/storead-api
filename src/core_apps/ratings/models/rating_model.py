from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.articles.models.article_model import Article
from core_apps.shared.models import TimeStampedModel

User = get_user_model()


class Rating(TimeStampedModel):
    RATING_CHOICES = [
        (1, _("Bad")),
        (2, _("Fair")),
        (3, _("Good")),
        (4, _("Very Good")),
        (5, _("Excellent")),
    ]
    article = models.ForeignKey(Article, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = ("article", "user")
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        db_table = "ratings"

    def get_rating_display(self):
        return self.RATING_CHOICES[self.rating - 1][1]

    def __str__(self):
        return f"{self.user.username} rated {self.article.title} as {self.get_rating_display()}"
