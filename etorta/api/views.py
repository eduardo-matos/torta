from django.shortcuts import render
from django.http import HttpResponse, Http404
from core.models import Produto, Url, Loja
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import LojaForm, ProdutoForm, ClienteForm, UrlForm
import json

# Create your views here.
def get(request, loja_id=0):

    get_object_or_404(Loja, pk=loja_id)

    produtos = list()

    for produto in Produto.objects.filter(loja=loja_id):

        prods = {
            'nome': produto.nome,
            'meu_preco': float(produto.meu_preco),
            'disponibilidade': produto.disponibilidade,
            'codigo': produto.codigo,
            'urls': []
        }

        for url in Url.objects.all().exclude(produto__exact=produto.pk):
            prods['urls'].append({
                'endereco': url.endereco,
                'preco': float(url.produto.meu_preco)
            })

        produtos.append(prods)

    return HttpResponse(json.dumps({
        'produtos': produtos
    }))


require_http_methods(['POST'])
def criar(request, tipo):

    if tipo == 'loja':
        form_class = LojaForm
    elif tipo == 'produto':
        form_class = ProdutoForm
    elif tipo == 'cliente':
        form_class = ClienteForm
    elif tipo == 'url':
        form_class = UrlForm
    else:
        raise Http404()

    form = form_class(request.POST)

    response = HttpResponse()

    if form.is_valid():
        form.save()
        response.status_code = 201
    else:
        response.status_code = 400
        response.content = json.dumps(dict(form.errors.items()))

    return response
