# Generated by Django 3.0.3 on 2020-03-30 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_tbl_movie_scores_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
    ]
