from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import pagination

class MoviePageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
