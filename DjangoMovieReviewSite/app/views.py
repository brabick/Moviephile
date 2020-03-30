"""
Definition of views.
"""

from django.shortcuts import render, redirect
from app import hidden_stuff
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
import requests

# Home page! Nothing interesting right now
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

# Same as home page
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

# straight forward sign up. Resides in the log in partial and its own form
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

# This is where we can view different reviews that are in the database.
# Depending on the information that is passed we will either
# Show 10 reviews by a user
# Show reviews of a specific movie
# or
# Show the 10 most recent reviews
# This is call controlled on where the user clicks and searches
def movie(request, id, is_movie, is_recent):
    assert isinstance(request, HttpRequest)
    if is_recent==1:
        movie = tbl_movie_scores.objects.all()[:10]
        header = "Recent Movie Reviews"
        message = "Here are the 10 most recent movie reviews"
    elif is_movie == 1:
        query = request.GET.get('search_string')
        movie = tbl_movie_scores.objects.filter(movie__movie_title__icontains=query)
        header = "All Reviews with '" + query + "' in the title"
        message = "noice"
    elif is_movie==0:
        movie = tbl_movie_scores.objects.filter(user=id)
        user = User.objects.get(id=id)
        header = "All Reviews by " + user.username
        message = user.username + " has reviewed quite a few movies!"
    
    return render(
        request,
        'app/movie.html',
        {
            'header':header,
            'movies':movie,
            'message': message,
            'year':datetime.now().year,
        }
    )

# Makes a request to the OMDb API and plops the search results into
# A page. The has clickable links to go to reviews of that movie
def search_results(request):
   assert isinstance(request, HttpRequest)
   query = request.GET.get('search_string') 
   # API request
   results = requests.get("http://www.omdbapi.com/?s=" + query + "&type=movie&apikey=" + hidden_stuff.API_KEY)
   results = results.json()
   info = results['Search']
   return render(
       request, 
       'app/search_results.html',
        {
        'movie_info': info,
        'null_message': 'There are no reviews for this movie, add one today!',
        'year':datetime.now().year,
        }
       )


# You gotta be in to create a review. Accesses the form created to add the review
# to the db
@login_required
def add_review(request, movie_id):
    assert isinstance(request, HttpRequest)
    movie = tbl_movies.objects.get(pk=movie_id)
    user = request.user
    if request.method=='POST':
        form = tbl_movie_scores_form(request.POST)
        if form.is_valid():
            review = form.save()
            # Calculates the total based off of the input scores
            review.total = (review.score + review.acting + review.cinematography + review.story_telling +
            review.plausibility + review.cast + review.effects + review.fun_factor + review.originality +
            review.characters)
            review.user_id = user.id
            review.movie_id = movie_id
            review.save()

            return redirect('view_review', movie_score_id=review.movie_score_id)
        else:
            
            return render(
            request,
            'app/add_review.html',
            {
            'form':form,
            'movie_info': movie,
            }
        )

    else:
        form = tbl_movie_scores_form()
        return render(
            request,
            'app/add_review.html',
            {
            'form':form,
            'movie_info': movie,
            }
        )

# View for viewing a review!
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