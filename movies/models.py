from __future__ import unicode_literals

import uuid

from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    uuid = models.UUIDField( _("UUID"), default=uuid.uuid4, editable=False,
                             db_index=True )

    class Meta:
        abstract = True


class Director(BaseModel):
    """
    This holds information about a director
    """
    name = models.CharField( _("Name of the Director"), max_length=70 )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Director")
        verbose_name_plural = _("Directors")


class Genre(BaseModel):
    """
    This holds all the available genres
    """
    genre = models.CharField( _("Genre"), max_length=30 )

    def __unicode__(self):
        return self.genre

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


class Movie(BaseModel):
    """
    This model holds all information about the movies
    """
    # Longest movie title till now is 58. We keep the max length at 70 to
    # accomodate names in the future that are a bit longer
    name = models.CharField( _("Name of the movie"), max_length=70 )
    director = models.ForeignKey( Director, verbose_name=_("director"),
                                  related_name=_("movies") )
    genres = models.ManyToManyField( Genre, verbose_name=_("genres"),
                                     related_name=_("movies") )
    duration = models.PositiveIntegerField( _("Duration of the movie in minutes"), )

    @property
    def rating(self):
        return self.ratings.aggregate(rating=models.Avg('rating'))['rating']

    @property
    def duration_string(self):
        return "{}h {}min".format(duration/60, duration%60)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")


class Rating(BaseModel):
    """
    Contains all the ratings for movies. The way this works is that users give
    ratings for individual movies. We store all the votes for a movie. These
    are then used to calculate the rating for the movie.
    An alternative approach could have been to just store the total rating and
    number of times the movie has been rated in the the 'Movie' table itself.
    But that was impractical as it would have created problems if two users
    tried to rate the movie simultaneously 
    """
    movie = models.ForeignKey( Movie, verbose_name=_("rating"), related_name=_("ratings") )
    rating = models.PositiveIntegerField( _("Rating"), validators=[MaxValueValidator(10),] )

    def __unicode__(self):
        return "{}: {}".format(self.movie.name, self.rating)

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
