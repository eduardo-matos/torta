from django.conf.urls import patterns, include, url
from .views import get

urlpatterns = patterns('',
    url(r'^get/(?P<loja_id>[\d]+)?$', get, name='get'),
)
