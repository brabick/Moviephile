from django.contrib import admin
from .models import tbl_category_desc, tbl_movie_scores

admin.site.register(tbl_movie_scores)
admin.site.register(tbl_category_desc)