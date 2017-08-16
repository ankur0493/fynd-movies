from __future__ import unicode_literals, print_function, absolute_import

from django.utils.translation import ugettext as _

from rest_framework import serializers, reverse

from movies.fields import UUIDField
from movies.models import Director, Genre, Movie


class DirectorSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse.reverse('api:v1:director-detail',
                               kwargs={'uuid': obj.uuid}, request=request)

    class Meta:
        model = Director
        fields = ('uuid', 'name', 'url')


class GenreSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse.reverse('api:v1:genre-detail',
                               kwargs={'uuid': obj.uuid}, request=request)

    class Meta:
        model = Genre
        fields = ('uuid', 'genre', 'url')


class BaseMovieSerializer(serializers.HyperlinkedModelSerializer):
    '''
    We use a base serializer and then extend it in different serializers for
    different REST methods for customization
    '''
    class Meta:
        model = Movie
        fields = ('url', 'name', 'director', 'genres', 'duration', 'rating', 'number_ratings')
        extra_kwargs = {
            'url': {'view_name': 'api:v1:movie-detail', 'lookup_field': 'uuid'}, 
            'director': {'view_name': 'api:v1:director-detail', 'lookup_field': 'uuid'},
            'genres': {'view_name': 'api:v1:genre-detail', 'lookup_field': 'uuid'},
        }


class MovieListSerializer(BaseMovieSerializer):
    director = DirectorSerializer()
    genres = GenreSerializer(many=True,)
    duration = serializers.CharField(source='duration_string')

    class Meta(BaseMovieSerializer.Meta):
        pass


class MovieCreateSerializer(BaseMovieSerializer):
    director = UUIDField()
    genres = serializers.ListField( child=UUIDField() )

    def create(self, validated_data):
        try:
            director_uuid = validated_data.pop('director', None)
            director = Director.objects.get(uuid=director_uuid)

            genres = [Genre.objects.get(uuid=uuid) for uuid in validated_data.pop('genres', [])]

            movie = Movie.objects.create(director=director, **validated_data)
            for genre in genres:
                movie.genres.add()
            return movie
        except Director.DoesNotExist, e:
            serializers.ValidationError( { 'director': _("Cannot retreive Director with given UUID") } )
        except Genre.DoesNotExist, e:
            serializers.ValidationError( { 'genres': _("Cannot retreive Genre with given UUID") } )

    class Meta(BaseMovieSerializer.Meta):
        pass


class MovieRetrieveSerializer(BaseMovieSerializer):
    director = DirectorSerializer()
    genres = GenreSerializer(many=True, source='genres.all')
    duration = serializers.CharField(source='duration_string')

    class Meta(BaseMovieSerializer.Meta):
        pass


class MovieUpdateDestroySerializer(BaseMovieSerializer):
    director = UUIDField()
    genres = serializers.ListField( child=UUIDField(), source='genres.all' )

    def update(self, instance, validated_data):
        try:
            director_uuid = validated_data.pop('director', None)
            director = Director.objects.get(uuid=director_uuid)

            instance.director = director

            genres = [Genre.objects.get(uuid=uuid) for uuid in validated_data.pop('genres', {}).get('all', [])]
            for genre in genres:
                if genre not in instance.genres.all():
                    instance.genres.add(genre)

            for attr, value in validated_data.items():
                    setattr(instance, attr, value)
            instance.save()

            return instance
        except Director.DoesNotExist:
            serializers.ValidationError( { 'director': _("Cannot retreive Director with given UUID") } )
        except Genre.DoesNotExist:
            serializers.ValidationError( { 'genres': _("Cannot retreive Genre with given UUID") } )

    class Meta(BaseMovieSerializer.Meta):
        pass
