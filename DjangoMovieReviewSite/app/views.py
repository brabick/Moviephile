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
    movie = tbl_movie_scores.objects.all()
    #movie = tbl_movie_scores.objects.values_list().distinct()

    return render(
        request,
        'app/about.html',
        {
            'movies':movie,
            'message':'Your application description.',
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

def movie(request, movie_id):
    assert isinstance(request, HttpRequest)
    movie = tbl_movie_scores.objects.filter(movie_id=movie_id)
    movie_title = tbl_movies.objects.get(pk=movie_id)
    return render(
        request,
        'app/movie.html',
        {
        'movie_info':movie,
        'title':movie_title,
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
        form = tbl_movie_scores_form(request.POST, {'user' : user.id, 'movie':movie_id})
        if form.is_valid():
            review = form.save()
            review.total = (review.score + review.acting + review.cinematography + review.story_telling +
            review.plausibility + review.cast + review.effects + review.fun_factor + review.originality +
            review.characters)
            review.save()
            return redirect('view_review', movie_score_id=review.movie_score_id)
    else:
        form = tbl_movie_scores_form({'user' : user.id, 'movie':movie_id})
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