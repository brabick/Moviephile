# Generated by Django 3.0.3 on 2020-03-01 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200227_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='review',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
