"""
Definition of views.
"""

from django.shortcuts import render, redirect
from app.models import tbl_movies, tbl_movie_scores
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from app.forms import SignUpForm, tbl_movie_scores_form
from django.contrib.auth import login, authenticate
from django.db.models import Sum
from django.contrib.auth.models import User


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        },
        
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    order_by = request.GET.get('order_by', 'created_at')
    movie = tbl_movie_scores.objects.all().order_by(order_by)[:10]
    return render(
        request,
        'app/about.html',
        {
            'movies':movie,
            'message':'Above are the ten most recent reviews! Click on a title to \
            see what made that movie so great.',
            'year':datetime.now().year,
        }
    )

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def movie(request, id, is_movie):
    assert isinstance(request, HttpRequest)
    if is_movie == 1:
        movie = tbl_movie_scores.objects.filter(movie_id=id)
        movie_title = tbl_movies.objects.get(movie_id=id)
        title = movie_title.movie_title
        header = "All Reviews of " + title
    elif is_movie==0:
        movie = tbl_movie_scores.objects.filter(user=id)
        user = User.objects.get(id=id)
        header = "All Reviews by " + user.username
    return render(
        request,
        'app/movie.html',
        {
            'header':header,
            'movie_info':movie,
            'null_message': 'There are no reviews for this movie, add one today!',
            'year':datetime.now().year,
        }
    )


def search_results(request):
   assert isinstance(request, HttpRequest)
   query = request.GET.get('search_string')
   results = tbl_movies.objects.filter(movie_title__icontains=query)
   return render(
       request, 
       'app/search_results.html',
        {
        'movie_info': results,
        'null_message': 'There are no reviews for this movie, add one today!',
        'year':datetime.now().year,
        }
       )

@login_required
def add_review(request, movie_id):
    assert isinstance(request, HttpRequest)
    movie = tbl_movies.objects.get(pk=movie_id)
    user = request.user
    if request.method=='POST':
        form = tbl_movie_scores_form(request.POST, {'user' : user.id, 'movie':movie_id, 'created_at':datetime.now(), 'updated_at':None})
        if form.is_valid():
            review = form.save()
            review.total = (review.score + review.acting + review.cinematography + review.story_telling +
            review.plausibility + review.cast + review.effects + review.fun_factor + review.originality +
            review.characters)
            review.save()
            return redirect('view_review', movie_score_id=review.movie_score_id)
    else:
        form = tbl_movie_scores_form({'user' : user.id, 'movie':movie_id, 'created_at':datetime.now(), 'updated_at':None})
        return render(
            request,
            'app/add_review.html',
            {
            'form':form,
            'movie_info': movie,
            }
        )

def view_review(request, movie_score_id):
    assert isinstance(request, HttpRequest)
    review = tbl_movie_scores.objects.get(pk=movie_score_id)
    return render(
        request,
        'app/view_review.html',
        {
            'review_info':review
        }
    )