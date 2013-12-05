from django.conf.urls import patterns, include, url
from .views import ProdutosView

urlpatterns = patterns('',
    url(r'^produtos/$', ProdutosView.as_view(), name='produtos'),
)
