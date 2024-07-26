from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.shared.models import TimeStampedModel


class Book(TimeStampedModel):
    isbn = models.CharField(verbose_name=_("ISBN"), max_length=255, unique=True)
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    author = models.CharField(verbose_name=_("Author"), max_length=255)
    published_date = models.DateField(verbose_name=_("Published Date"))
    description = models.TextField(verbose_name=_("Description"))
    thumbnail_url = models.ImageField(
        verbose_name=_("Thumbnail"),
        upload_to="book_thumbnails",
        default="default_book.png",
    )

    class Meta:
        db_table = "books"
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

        indexes = [
            models.Index(
                fields=[
                    "isbn",
                ]
            ),
            models.Index(
                fields=[
                    "title",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"
