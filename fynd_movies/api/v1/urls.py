from django.conf.urls import url, include

urlpatterns =  [
    url('^', include('movies.api.v1.urls')),
]
