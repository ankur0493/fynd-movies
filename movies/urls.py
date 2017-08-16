from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url('^$', TemplateView.as_view(template_name='index.html')),
    url('^login/$', TemplateView.as_view(template_name='login.html')),
]
