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
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    path('movie/<int:id>/<int:is_movie>/<int:is_recent>', app.views.movie, name='movie'),
    url(r'^signup/$', app.views.signup, name='signup'),   
    url(r'^login/$',
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
    url(r'^logout$',
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
    path('search_results/<int:is_review>', app.views.search_results, name='search_results'),
    url(r'^add_review/(?P<movie_id>\w+)/$', app.views.add_review, name='add_review'),
    url(r'^view_review/(?P<movie_score_id>\w+)/$', app.views.view_review, name='view_review'),
]
