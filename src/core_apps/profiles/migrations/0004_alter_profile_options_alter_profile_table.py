# Generated by Django 4.2.11 on 2024-06-23 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_profile_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
        migrations.AlterModelTable(
            name='profile',
            table='profiles',
        ),
    ]