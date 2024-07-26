# Generated by Django 4.2.11 on 2024-05-27 07:48

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                allow_unicode=True, always_update=True, editable=False, populate_from="title", unique=True
            ),
        ),
    ]
