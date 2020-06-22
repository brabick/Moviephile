"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class tbl_movie_scores(models.Model):
    movie_score_id = models.AutoField(primary_key=True)
    movie_id = models.CharField(max_length=40, blank=True, null=True)
    title = models.CharField(max_length=200, null=True)
    sound = models.IntegerField(validators=[
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
    poster = models.CharField(max_length=200, null=True)

class tbl_category_desc(models.Model):
     category = models.CharField(max_length=200, null=True)
     description = models.TextField(blank=True, null=True)

class tbl_user_last_search(models.Model):
        session_key = models.CharField(max_length=200, null=True)
        last_search = models.CharField(max_length=200, null=True)
        updated_at = models.DateTimeField(auto_now=True, null=True)
