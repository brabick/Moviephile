# Generated by Django 3.0.3 on 2020-02-27 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20200225_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_movie_scores',
            name='user_id',
        ),
        migrations.AddField(
            model_name='tbl_movie_scores',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
