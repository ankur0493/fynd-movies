from django.conf.urls import include, url

urlpatterns = [
    url(r'v1/', include('fynd_movies.api.v1.urls', namespace='v1')),
]
