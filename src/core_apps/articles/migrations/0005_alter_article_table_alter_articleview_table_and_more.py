# Generated by Django 4.2.11 on 2024-06-23 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0004_alter_article_slug"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="article",
            table="article",
        ),
        migrations.AlterModelTable(
            name="articleview",
            table="article_view",
        ),
        migrations.AlterModelTable(
            name="recommend",
            table="recommend",
        ),
    ]
