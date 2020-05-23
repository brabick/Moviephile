"""
Definition of urls for DjangoMovieReviewSite.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.contrib import admin
import app.forms
import app.views
from django.urls import include, path


# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    path('', app.views.home, name='home'),
    path('home/<int:bad_search>', app.views.home, name='home'),
    path('contact', app.views.contact, name='contact'),
    path('about', app.views.about, name='about'),
    path('movie/<str:id>/', app.views.movie, name='movie'),
    path('signup', app.views.signup, name='signup'),   
    path('login',
        django.contrib.auth.views.LoginView.as_view(),
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    path('logout',
        django.contrib.auth.views.LogoutView.as_view(),
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]

urlpatterns = urlpatterns + [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search_results/', app.views.search_results, name='search_results'),
    path('add_review/<str:movie_id>/', app.views.add_review, name='add_review'),
    path('view_review/<int:movie_score_id>/', app.views.view_review, name='view_review'),
    path('user/<int:user_id>/', app.views.user, name="user"),
    path('reviews/', app.views.reviews, name="reviews")
]
