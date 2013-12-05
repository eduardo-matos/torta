from django.conf.urls import patterns, include, url
from .views import ProdutosView, ProdutoCriarView, ProdutoAtualizarView

urlpatterns = patterns('',
    url(r'^produtos/$', ProdutosView.as_view(), name='produtos'),
    url(r'^produto/criar/$', ProdutoCriarView.as_view(), name='produto-criar'),
    url(r'^produto/atualizar/(?P<pk>\d+)$', ProdutoAtualizarView.as_view(), name='produto-atualizar'),
)
