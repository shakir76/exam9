# Generated by Django 4.1.1 on 2022-09-24 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='album',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='webapp.album', verbose_name='Альбом'),
        ),
    ]
