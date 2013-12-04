from django.conf.urls import patterns, include, url
from .views import get, criar, atualizar

urlpatterns = patterns('',
    url(r'^get/(?P<loja_id>[\d]+)?$', get, name='get'),
    url(r'^post/([a-z]+)/$', criar, name='criar'),
    url(r'^put/([a-z]+)/(\d+)/$', atualizar, name='atualizar'),
)
