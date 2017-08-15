from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import  url, include

from .views import MovieListView

urlpatterns = [
    url(r'^movies/$', MovieListView.as_view(), name='movie-list'),
]
