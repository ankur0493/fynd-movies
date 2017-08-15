from __future__ import unicode_literals, print_function, absolute_import

from django.utils.translation import ugettext as _

from rest_framework import (
    generics, serializers, permissions, filters, response, status, exceptions
)

from movies.models import Movie
from .pagination import MoviePageNumberPagination


class MovieListView(generics.ListCreateAPIView):
    # We needed to override the default permission class to provide 'page_size'
    pagination_class = MoviePageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    # The IsAuthenticated permission checks if the user is logged in or not
    # The IsAdminUser permission allows access only to staff users (is_staff=True)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        '''
        We use different serializers for GET (ListView) and for POST (CreateView)
        '''
        if self.request.method == 'GET':
            return MovieListSerializer

        # Covers POST
        return MovieCreateSerializer
