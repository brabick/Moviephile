# Generated by Django 3.0.3 on 2020-02-26 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='acting',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='cast',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='characters',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='cinematography',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='effects',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='fun_factor',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='originality',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='plausibility',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='score',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='story_telling',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tbl_movie_scores',
            name='total',
            field=models.IntegerField(),
        ),
    ]