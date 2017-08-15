from __future__ import unicode_literals, print_function, absolute_import

from django.utils.translation import ugettext as _

from rest_framework import serializers, reverse

from movies.models import Movie


class BaseMovieSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse.reverse('api:v1:movie-detail',
                               kwargs={'uuid': obj.uuid}, request=request)

    class Meta:
        model = Movie
        fields = ('url', 'name', 'director', 'genres', 'duration')
