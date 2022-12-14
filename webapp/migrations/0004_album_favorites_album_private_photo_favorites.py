# Generated by Django 4.1.1 on 2022-09-24 06:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0003_alter_photo_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='favorites',
            field=models.ManyToManyField(related_name='favorites_album', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='album',
            name='private',
            field=models.BooleanField(default=False, verbose_name='Приватный'),
        ),
        migrations.AddField(
            model_name='photo',
            name='favorites',
            field=models.ManyToManyField(related_name='favorites_photo', to=settings.AUTH_USER_MODEL),
        ),
    ]
