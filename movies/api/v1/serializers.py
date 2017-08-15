from __future__ import unicode_literals, print_function, absolute_import

from django.utils.translation import ugettext as _

from rest_framework import serializers, reverse

from movies.models import Director, Genre, Movie


class DirectorSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse.reverse('api:v1:director-detail',
                               kwargs={'uuid': obj.uuid}, request=request)

    class Meta:
        model = Director
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse.reverse('api:v1:genre-detail',
                               kwargs={'uuid': obj.uuid}, request=request)

    class Meta:
        model = Genre
        fields = '__all__'


class BaseMovieSerializer(serializers.HyperlinkedModelSerializer):
    '''
    We use a base serializer and then extend it in different serializers for
    different REST methods for customization
    '''
    class Meta:
        model = Movie
        fields = ('url', 'name', 'director', 'genres', 'duration', 'rating')
        extra_kwargs = {
            'url': {'view_name': 'api:v1:movie-detail', 'lookup_field': 'uuid'}, 
            'director': {'view_name': 'api:v1:director-detail', 'lookup_field': 'uuid'},
            'genres': {'view_name': 'api:v1:genre-detail', 'lookup_field': 'uuid'},
        }


class MovieListCreateSerializer(BaseMovieSerializer):
    class Meta(BaseMovieSerializer.Meta):
        pass


class MovieRetrieveUpdateDestroySerializer(BaseMovieSerializer):
    class Meta(BaseMovieSerializer.Meta):
        pass
