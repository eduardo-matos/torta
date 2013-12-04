from django.conf.urls import patterns, include, url
from .views import get, criar, atualizar, remover

urlpatterns = patterns('',
    url(r'^get/(?P<loja_id>[\d]+)?/$', get, name='get'),
    url(r'^post/([a-z]+)/$', criar, name='criar'),
    url(r'^put/([a-z]+)/(\d+)/$', atualizar, name='atualizar'),
    url(r'^del/([a-z]+)/(\d+)/$', remover, name='remover'),
)
