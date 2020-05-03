"""
Definition of views.
"""

from django.shortcuts import render, redirect
from app import hidden_stuff
from app.models import tbl_movie_scores, tbl_category_desc
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
from django.template import Library

# Home page!  Nothing interesting right now
def home(request, bad_search='0'):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if bad_search==1:
        search='Something went wrong with the search, please try again.'
    else:
        search=''
    return render(request,
        'app/index.html',
        {
            'title':'Home Page',
            'search':search,
            'year':datetime.now().year,
        },)

# Same as home page
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'I like movies and coding',
            'year':datetime.now().year,
        })


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    desc = tbl_category_desc.objects.all()
    return render(request,
        'app/about.html',
        {  
            'desc': desc,
            'message':'Above are the ten most recent reviews! Click on a title to \
            see what made that movie so great.',
            'year':datetime.now().year,
        })

# straight forward sign up.  Resides in the log in partial and its own form
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
def movie(request, id, is_recent):
    assert isinstance(request, HttpRequest)
    null_message = ''
    # If we are just getting the recent movie reviews
    if is_recent == 1:
        movie = tbl_movie_scores.objects.all()[:20]
        header = "Recent Movie Reviews"
        message = "Here are the 20 most recent movie reviews, is one of yours here?"
    # If we are searching for reviews by a specific user
    else:
        movie = tbl_movie_scores.objects.filter(user=id)
        user = User.objects.get(id=id)
        header = "All Reviews by " + user.username
        message = user.username + " has reviewed quite a few movies!"
    
    return render(request,
        'app/movie.html',
        {
            'header':header,
            'movies':movie,
            'message': message,
            'null_message': null_message,
            'year':datetime.now().year,
        })

# Makes a request to the OMDb API and plops the search results into
# A page.  The has clickable links to go to reviews of that movie
def search_results(request):
   assert isinstance(request, HttpRequest)
   query = request.GET.get('search_string') 
   # API request
   results = requests.get("http://www.omdbapi.com/?s=" + query + "&type=movie&apikey=" + hidden_stuff.API_KEY)
   results = results.json()
   if results.get('Search') == "Incorrect IMDb ID.":
       return redirect('home', bad_search=1)
   if 'Error' in results:
       error = results.get('Error')
       if error == 'Incorrect IMDb ID.':
            return redirect('home', bad_search=1)
       elif error == 'Too many results.':
            # It's a bit sketchy, but if we get too many results, we just go
            # To the most popular result for what the person searched
            # At least this way we won't get and error
            results = requests.get("http://www.omdbapi.com/?t=" + query + "&type=movie&apikey=" + hidden_stuff.API_KEY)
            results = results.json()
            return redirect('add_review', movie_id=results.get('imdbID'))
       
   else:
       info = results['Search']
       review_info = tbl_movie_scores.objects.filter(title__icontains=query)
       movie_header = "Movies with '" + query + "' in the title"
       review_header = "Reviews with '" + query + "' in the title"
       return render(request, 
           'app/search_results.html',
            {
            'movie_info': info,
            'movie_header': movie_header,
            'review_info': review_info,
            'review_header': review_header,
            'null_message': 'There are no reviews for this movie, add one today!',
            'year':datetime.now().year,
            })


# You gotta be in to create a review.  Accesses the form created to add the
# review
# to the db
@login_required
def add_review(request, movie_id):
    assert isinstance(request, HttpRequest)
    if movie_id == 'None':
        return redirect('home', bad_search=1)
    movie = requests.get("http://www.omdbapi.com/?i=" + movie_id + "&plot=full&apikey=" + hidden_stuff.API_KEY)
    movie = movie.json()
    user = request.user
    add_review = 1
    reviews = tbl_movie_scores.objects.filter(movie_id=movie_id)
    if request.method == 'POST':
        form = tbl_movie_scores_form(request.POST)
        if form.is_valid():
            review = form.save()
            # Calculates the total based off of the input scores
            review.total = (review.sound + review.acting + review.cinematography + review.story_telling + review.plausibility + review.cast + review.effects + review.fun_factor + review.originality + review.characters)
            review.user_id = user.id
            review.movie_id = movie.get('imdbID')
            review.title = movie.get('Title')
            review.save()

            return redirect('view_review', movie_score_id=review.movie_score_id)
        else:
            
            return render(request,
            'app/view_review.html',
            {
            'reviews':reviews,
            'form':form,
            'movie_info': movie,
            'add_review': add_review,
            'header': movie.get('Title') + ', ' + movie.get('Year')
            })

    else:
        form = tbl_movie_scores_form()
        return render(request,
            'app/view_review.html',
            {
            'reviews':reviews,
            'form':form,
            'movie_info': movie,
            'add_review': add_review,
            'header': movie.get('Title') + ', ' + movie.get('Year')
            })

# View for viewing a review!
def view_review(request, movie_score_id):
    assert isinstance(request, HttpRequest)
    review = tbl_movie_scores.objects.get(pk=movie_score_id)
    id = review.movie_id
    reviews = tbl_movie_scores.objects.filter(movie_id=id)
    movie = requests.get("http://www.omdbapi.com/?i=" + id + "&plot=full&apikey=" + hidden_stuff.API_KEY)
    movie = movie.json()
    add_review = 0
    return render(request,
        'app/view_review.html',
        {
            'reviews':reviews,
            'movie_info': movie,
            'review_info':review,
            'add_review':add_review,
            'total': range(review.total),
            'header': 'Review for ' + movie.get('Title')
        })

register = Library()

@register.filter
def get_range(value):
    return range(value)

def page_not_found(request):
    return render('404.html')
def server_error(request):
    return render('500.html')