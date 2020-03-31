"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class tbl_movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_title = models.CharField(max_length=80)
    movie_genre = models.CharField(max_length=80)
    movie_release_year = models.CharField(max_length=80)
    movie_poster = models.ImageField(null=True)

class tbl_movie_scores(models.Model):
    movie_id = models.CharField(max_length=40, null=True)
    title = models.CharField(max_length=200, null=True)
    movie_score_id = models.AutoField(primary_key=True)
    score = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    cinematography = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    story_telling = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    acting = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    plausibility = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    cast = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    effects = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    fun_factor = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    originality = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    characters = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)])
    total = models.IntegerField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


