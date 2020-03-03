"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class tbl_movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_title = models.CharField(max_length=80)
    movie_genre = models.CharField(max_length=80)
    movie_release_year = models.CharField(max_length=80)

class tbl_movie_scores(models.Model):
    movie = models.ForeignKey(tbl_movies, on_delete=models.CASCADE)
    movie_score_id = models.AutoField(primary_key=True)
    score = models.IntegerField()
    cinematography = models.IntegerField()
    story_telling = models.IntegerField()
    acting = models.IntegerField()
    plausibility = models.IntegerField()
    cast = models.IntegerField()
    effects = models.IntegerField()
    fun_factor = models.IntegerField()
    originality = models.IntegerField()
    characters = models.IntegerField()
    total = models.IntegerField(blank=True, null=True)
    review = models.CharField(max_length=4000, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


