# Generated by Django 3.0.3 on 2020-04-23 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20200409_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_catagory_desc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sound', models.TextField(blank=True, null=True)),
                ('cinematography', models.TextField(blank=True, null=True)),
                ('story_telling', models.TextField(blank=True, null=True)),
                ('acting', models.TextField(blank=True, null=True)),
                ('plausibility', models.TextField(blank=True, null=True)),
                ('cast', models.TextField(blank=True, null=True)),
                ('effects', models.TextField(blank=True, null=True)),
                ('fun_factor', models.TextField(blank=True, null=True)),
                ('originality', models.TextField(blank=True, null=True)),
                ('characters', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='tbl_movies',
        ),
    ]
