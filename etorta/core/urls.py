from django.conf.urls import patterns, include, url
from .views import ProdutosView, ProdutoCriarView

urlpatterns = patterns('',
    url(r'^produtos/$', ProdutosView.as_view(), name='produtos'),
    url(r'^produto/criar/$', ProdutoCriarView.as_view(), name='produto-criar'),
)
