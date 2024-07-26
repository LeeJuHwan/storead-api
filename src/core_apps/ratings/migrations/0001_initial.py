# Generated by Django 4.2.11 on 2024-04-26 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rating",
            fields=[
                ("pkid", models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Bad"), (2, "Fair"), (3, "Good"), (4, "Very Good"), (5, "Excellent")]
                    ),
                ),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="ratings", to="articles.article"
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Rating",
                "verbose_name_plural": "Ratings",
                "unique_together": {("article", "user")},
            },
        ),
    ]
