# Generated by Django 4.2.11 on 2024-04-25 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='thumbnail_url',
            field=models.ImageField(default='default_book.png', upload_to='book_thumbnails', verbose_name='Thumbnail'),
        ),
        migrations.AlterModelTable(
            name='book',
            table='books',
        ),
    ]