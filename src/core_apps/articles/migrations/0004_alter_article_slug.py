# Generated by Django 4.2.11 on 2024-05-27 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0003_alter_article_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=models.SlugField(allow_unicode=True, unique=True),
        ),
    ]
