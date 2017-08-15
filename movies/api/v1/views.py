from __future__ import unicode_literals, print_function, absolute_import

from django.utils.translation import ugettext as _

from rest_framework import (
    generics, serializers, permissions, filters, response, status, exceptions
)

from movies.models import Director, Genre, Movie
from .pagination import MoviePageNumberPagination
from .serializers import (
    DirectorSerializer, GenreSerializer, MovieListCreateSerializer,
    MovieRetrieveUpdateDestroySerializer,
)


class DirectorListView(generics.ListCreateAPIView):
    pagination_class = MoviePageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()


class DirectorDetailView(generics.RetrieveUpdateAPIView):
    pagination_class = MoviePageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    lookup_field = 'uuid'

class GenreListView(generics.ListCreateAPIView):
    pagination_class = MoviePageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class GenreDetailView(generics.RetrieveUpdateAPIView):
    pagination_class = MoviePageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = 'uuid'


class MovieListView(generics.ListCreateAPIView):
    # We needed to override the default permission class to provide 'page_size'
    pagination_class = MoviePageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    # The IsAuthenticated permission checks if the user is logged in or not
    # The IsAdminUser permission allows access only to staff users (is_staff=True)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
    serializer_class = MovieListCreateSerializer
    queryset = Movie.objects.all()


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    # We needed to override the default permission class to provide 'page_size'
    pagination_class = MoviePageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    # The IsAuthenticated permission checks if the user is logged in or not
    # The IsAdminUser permission allows access only to staff users (is_staff=True)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
    serializer_class = MovieRetrieveUpdateDestroySerializer
    queryset = Movie.objects.all()

