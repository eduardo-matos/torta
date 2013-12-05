from django.conf.urls import patterns, include, url
from .views import (ProdutosView, ModelCriarView,
	ModelAtualizarView, ModelRemoverView, HomeView, LoginView)

urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'core.views.logout', name='logout'),
    url(r'^produtos/$', ProdutosView.as_view(), name='produtos'),
    url(r'^(?P<tipo>[a-z]+)/criar/$', ModelCriarView.as_view(), name='model-criar'),
    url(r'^(?P<tipo>[a-z]+)/atualizar/(?P<pk>\d+)$', ModelAtualizarView.as_view(), name='model-atualizar'),
    url(r'^(?P<tipo>[a-z]+)/remover/(?P<pk>\d+)$', ModelRemoverView.as_view(), name='model-remover'),
    url(r'^$', HomeView.as_view(), name='home'),
)
