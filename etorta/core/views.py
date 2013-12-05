from django.views.generic import ListView
from .models import Produto

class ProdutosView(ListView):
    template_name = 'core/produtos.html'
    model = Produto
    context_object_name = 'produtos'
