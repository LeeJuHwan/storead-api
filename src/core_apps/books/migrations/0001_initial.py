# Generated by Django 4.2.11 on 2024-04-20 09:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('isbn', models.CharField(max_length=255, unique=True, verbose_name='ISBN')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('author', models.CharField(max_length=255, verbose_name='Author')),
                ('published_date', models.DateField(verbose_name='Published Date')),
                ('description', models.TextField(verbose_name='Description')),
                ('thumbnail_url', models.ImageField(upload_to='book_thumbnails', verbose_name='Thumbnail')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
    ]
