"""
Definition of views.
"""

from django.shortcuts import render, redirect
from app import hidden_stuff
from app.models import tbl_movie_scores, tbl_category_desc, tbl_user_last_search
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from app.forms import SignUpForm, tbl_movie_scores_form
from django.contrib.auth import login, authenticate
from django.db.models import Sum
from django.contrib.auth.models import User
import requests
from django import template
from django.http import HttpResponseRedirect
from django.contrib import messages


# Home page!  Nothing interesting right now
def home(request, bad_search='0'):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    movie = tbl_movie_scores.objects.all().order_by("-movie_score_id")[:3]
    totals = movie.values_list('total', flat=True)
    totals = list(totals)
    ranges = [range(totals[0]), range(totals[1]), range(totals[2])]
    if bad_search==1:
        search='Something went wrong with the search, please try again.'
    else:
        search=''
    return render(request,
        'app/index.html',
        {
            'movies':movie,
            'title':'Home Page',
            'search':search,
            'year':datetime.now().year,
            'total':ranges,
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
def movie(request, id):
    assert isinstance(request, HttpRequest)
    null_message = ''
    # If we are searching for reviews by a specific user
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
# Makes a request to the OMDb API and plops the search results into a list of at most 50 results
def search_results(request, page):
   assert isinstance(request, HttpRequest)
   # retrive the search string   
   query = request.GET.get('search_string')        
   query = query.strip()
   movie_header = "Movies related to '" + query + "'"
   review_header = "Reviews related to '" + query + "'"
   review_info = tbl_movie_scores.objects.filter(title__icontains=query)

   # initial request
   results = requests.get(
       "http://www.omdbapi.com/?s=" + query + "&type=movie&apikey=" + hidden_stuff.API_KEY)
   results = results.json()
   # if there is a space in the search, we can guarantee results, even if the user does something weird
   # Unless they just enter jibberish
   # Here, we split the query into a list
   if ' ' in query:
       query = query.split(' ')
   # if the user only gave us one word in the query, there isn't much we can do (for now)
   # redirect with an error message
   if results.get('Response') == 'False' and len(query) == 1:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), messages.info(request, 'Your search failed, how about we try again?'))
   # If the entered a couple of words, we can iterate through them and make a request for each one
   # If one of them comes back with results, great! we replace the results variable with that search and keep going
   elif isinstance(query, list) and len(query) > 1:
       for q in query:
           results = requests.get(
               "http://www.omdbapi.com/?s=" + q + "&type=movie&apikey=" + hidden_stuff.API_KEY)
           results = results.json()
           if 'Search' in results:
               break

   # Goes through the query list and makes a request for each item
   # If there are results in there, we add them to results['Search'], otherwise, who cares?
   if 'totalResults' in results:
       pages = round(int(results['totalResults']) / 10)
   else:
       pages = 0
   if not isinstance(query, list):
       results = requests.get(
           "http://www.omdbapi.com/?s=" + query + "&type=movie&apikey=" + hidden_stuff.API_KEY)
       results = results.json()
       get_all_page_results(pages, results, query)
   else:
       for q in query:
           r = requests.get(
               "http://www.omdbapi.com/?s=" + q + "&type=movie&apikey=" + hidden_stuff.API_KEY)
           r = r.json()
           if 'Search' in r:
               for dict in r['Search']:
                   if dict not in results['Search']:
                       results['Search'].append(dict)
                   get_all_page_results(pages, results, q)
           else:
               continue

   if results.get('Response') == 'False':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), messages.info(request, 'Your search failed, how about we try again?'))
   else:
       info = results['Search'][0:]
       response = render(request, 
           'app/search_results.html',
            {
            'movie_info': info,
            'movie_header': movie_header,
            'movies': review_info,
            'review_header': review_header,
            'null_message': 'There are no reviews for this movie, add one today!',
            'year':datetime.now().year,
            })
       response.set_cookie('last_search', query)
       return response

# Function to get all data from multiple pages
def get_all_page_results(pages, results_set, query):
    for p in range(int(pages)):
        p = p + 1
        p = str(p)
        r = requests.get(
            "http://www.omdbapi.com/?s=" + query + "&page=" + p + "&type=movie&apikey=" + hidden_stuff.API_KEY)
        r = r.json()
        if 'Search' in r:
            for res in r['Search']:
                if res not in results_set['Search']:
                    results_set['Search'].append(res)
            if p == str(4):
                break
        else:
            continue
    return results_set

# You gotta be in to create a review.  Accesses the form created to add the
# review
# to the db
@login_required
def add_review(request, movie_id):
    assert isinstance(request, HttpRequest)
    if movie_id == 'None':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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
            review.poster = movie.get('Poster')
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
            'header': movie.get('Title') + ', ' + movie.get('Year'),
            'year':datetime.now().year,
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
            'header': movie.get('Title') + ', ' + movie.get('Year'),
            'year':datetime.now().year,
            })

# View for viewing a review!
def view_review(request, movie_score_id):
    assert isinstance(request, HttpRequest)
    review = tbl_movie_scores.objects.get(pk=movie_score_id)
    descs = tbl_category_desc.objects.all()
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
            'header': 'Review for ' + movie.get('Title'),
            'description': descs,
            'year':datetime.now().year,
        })

@login_required
def user(request, user_id):
    assert isinstance(request, HttpRequest)
    if not User.objects.filter(id=user_id).exists():
        return redirect('user', request.user.id)
    review_info = tbl_movie_scores.objects.filter(user=user_id)
    review_count = review_info.count()
    user_info = User.objects.get(id=user_id)
    current_user = request.user
    #if user_id != current_user.id:
    return render(request,
    'app/user.html',
    {
        'movies':review_info,
        'reviews':review_count,
        'user_info':user_info,
        'year':datetime.now().year,
    })

def reviews(request):
    assert isinstance(request, HttpRequest)
    reviews = tbl_movie_scores.objects.all()
    reviews_count = reviews.count()
    if reviews_count > 50:
        reviews_count = 50
    return render(request,
    'app/reviews.html',
    {
        'movies':reviews[:reviews_count],
        'year':datetime.now().year,
    })



def page_not_found(request):
    return render('404.html')
def server_error(request):
    return render('500.html')