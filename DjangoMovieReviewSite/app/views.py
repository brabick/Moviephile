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
# Makes a request to the OMDb API and plops the search results into
# A page.  The has clickable links to go to reviews of that movie
def search_results(request, page):
   assert isinstance(request, HttpRequest)
   # retrive the search string   
   query = request.GET.get('search_string')        
   if query == None:
       query = request.COOKIES.get('last_search')
   else:
       query = query.strip()
   page = str(page)
   # API request
   results = requests.get("http://www.omdbapi.com/?s=" + query + "&page=" + page + "&type=movie&apikey=" + hidden_stuff.API_KEY)
   results = results.json()
   message=''
   if results.get('Search') == "Incorrect IMDb ID.":
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'), messages.info(request, 'Something went horribly wrong'))
   if results.get('Response') == 'False':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), messages.info(request, 'Your search failed, how about we try again?'))
   if 'Error' in results:
       error = results.get('Error')
       if error == 'Incorrect IMDb ID.':
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       elif error == 'Too many results.':
            # It's a bit sketchy, but if we get too many results, we just go
            # To the most popular result for what the person searched
            # At least this way we won't get and error
            results = requests.get("http://www.omdbapi.com/?t=" + query + "&page=" + page + "&type=movie&apikey=" + hidden_stuff.API_KEY)
            results = results.json()
            return redirect('add_review', movie_id=results.get('imdbID'))
      
   else:
       num_results = int(results.get('totalResults'))
       if num_results > 10:
           num_results = num_results / 10
           page_num = round(num_results)
           page_str = str(page_num)
           results = requests.get("http://www.omdbapi.com/?s=" + query + "&page=" + page + "&type=movie&apikey=" + hidden_stuff.API_KEY)
           results = results.json()
           info = results['Search']
           if page_num >= 6:
               page_num = 6
       else:
           info = results['Search']
           page_num = 0
       review_info = tbl_movie_scores.objects.filter(title__icontains=query)
       movie_header = "Movies with '" + query + "' in the title"
       review_header = "Reviews with '" + query + "' in the title"
       response = render(request, 
           'app/search_results.html',
            {
            'movie_info': info,
            'movie_header': movie_header,
            'movies': review_info,
            'review_header': review_header,
            'null_message': 'There are no reviews for this movie, add one today!',
            'year':datetime.now().year,
            'pages':range(1, int(page_num))
            })
       response.set_cookie('last_search', query)
       return response


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