from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from ..books.models import Book
from ..common.models import TimeStampedModel
from ..social_users.models import SocialUser
from .read_time_engine import ArticleReadTimeEngine


class Recommend(TimeStampedModel):
    user = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="article_recommends")

    class Meta:
        verbose_name = _("Recommendation")
        verbose_name_plural = _("Recommendations")
        unique_together = ["user", "article"]
        ordering = ["-created_at"]
        db_table = "recommend"

    def __str__(self):
        return f"{self.user.username} recommends {self.article.title}"


class ArticleView(TimeStampedModel):
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="article_views")
    user = models.ForeignKey(SocialUser, on_delete=models.SET_NULL, null=True, related_name="user_views")
    viewer_ip = models.GenericIPAddressField(verbose_name=_("viewer IP"), null=True, blank=True)

    class Meta:
        verbose_name = _("Article View")
        verbose_name_plural = _("Article Views")
        unique_together = ("article", "user", "viewer_ip")
        db_table = "article_view"

    def __str__(self):
        return f"{self.article.title} viewed by {self.user.username if self.user else 'Anonymous'}"

    @classmethod
    def record_view(cls, article, user, viewer_ip):
        view, _ = cls.objects.get_or_create(article=article, user=user, viewer_ip=viewer_ip)
        view.save()


class Article(TimeStampedModel):
    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name="articles")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, related_name="books", null=True)
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.CharField(verbose_name=_("description"), max_length=255)
    body = models.TextField(verbose_name=_("article content"))

    tags = TaggableManager()

    recommends = models.ManyToManyField(SocialUser, through=Recommend, related_name="recommends")

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Article")
        db_table = "article"

    def __str__(self):
        return f"{self.author.username}'s {self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def estimated_reading_time(self) -> str:
        return ArticleReadTimeEngine.estimate_reading_time(self)

    def view_count(self) -> int:
        return self.article_views.count()

    def view_recommends(self) -> int:
        return self.article_recommends.count()

    def author_rating(self):
        author_rating = self.ratings.filter(user=self.author).first()
        if author_rating:
            return author_rating.rating
        return None
