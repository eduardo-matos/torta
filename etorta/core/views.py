from django.http import Http404
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Produto
from api.forms import ProdutoForm
from django.core.urlresolvers import reverse_lazy as r
from api.views import get_model_e_form_por_tipo


class HomeView(TemplateView):
    template_name = 'core/home.html'


class ProdutosView(ListView):
    template_name = 'core/produtos.html'
    model = Produto
    context_object_name = 'produtos'


class ModelCriarView(CreateView):
    template_name = 'core/model-criar.html'
    success_url = r('core:produtos')

    def form_valid(self, form):
        form.save()
        return super(ModelCriarView, self).form_valid(form)

    def get_form_class(self):
        form_class, _ = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return form_class


class ModelAtualizarView(UpdateView):
    template_name = 'core/model-criar.html'
    success_url = r('core:produtos')

    def form_valid(self, form):
        form.save()
        return super(ModelAtualizarView, self).form_valid(form)

    def get_queryset(self):
        _, model_class = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return model_class.objects.all()

    def get_form_class(self):
        form_class, _ = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return form_class


class ModelRemoverView(DeleteView):
    template_name = 'core/model-remover.html'
    success_url = r('core:produtos')

    def get_model(self):
        _, model_class = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return model_class

    def get_queryset(self):
        _, model_class = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return model_class.objects.all()
