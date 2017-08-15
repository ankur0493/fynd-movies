from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import  url, include

from .views import (
    DirectorListView, DirectorDetailView, GenreListView, GenreDetailView,
    MovieListView, MovieDetailView,
)


urlpatterns = [
    # Director
    url(r'^directors/$', DirectorListView.as_view(), name='director-list'),
    url(r'^directors/(?P<uuid>[a-zA-Z0-9-]+)/$', DirectorDetailView.as_view(), name='director-detail'),

    # Genre
    url(r'^genres/$', GenreListView.as_view(), name='genre-list'),
    url(r'^genres/(?P<uuid>[a-zA-Z0-9-]+)/$', GenreDetailView.as_view(), name='genre-detail'),

    # Movie
    url(r'^movies/$', MovieListView.as_view(), name='movie-list'),
    url(r'^movies/(?P<uuid>[a-zA-Z0-9-]+)/$', MovieDetailView.as_view(), name='movie-detail'),
]
