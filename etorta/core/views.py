from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Produto
from api.forms import ProdutoForm
from django.core.urlresolvers import reverse_lazy as r

class ProdutosView(ListView):
    template_name = 'core/produtos.html'
    model = Produto
    context_object_name = 'produtos'


class ProdutoCriarView(CreateView):
    template_name = 'core/produtos-criar.html'
    form_class = ProdutoForm
    success_url = r('core:produtos')

    def form_valid(self, form):
        produto = form.save()
        return super(ProdutoCriarView, self).form_valid(form)


class ProdutoAtualizarView(UpdateView):
    template_name = 'core/produtos-criar.html'
    form_class = ProdutoForm
    success_url = r('core:produtos')

    def form_valid(self, form):
        produto = form.save()
        return super(ProdutoAtualizarView, self).form_valid(form)

    def get_queryset(self):
        return Produto.objects.all().filter(pk=self.kwargs['pk'])


class ProdutoRemoverView(DeleteView):
    model = Produto
    template_name = 'core/produtos-remover.html'
    success_url = r('core:produtos')
    context_object_name = 'produto'
