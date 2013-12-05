from django.shortcuts import render
from django.http import HttpResponse, Http404
from core.models import Produto, Url, Loja, Cliente
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from .forms import LojaForm, ProdutoForm, ClienteForm, UrlForm
import json
from urlparse import parse_qsl

# Create your views here.
def get(request, loja_id=0):

    loja = get_object_or_404(Loja, pk=loja_id)

    produtos = list()

    for produto in loja.produtos.all():

        urls_deste_produto_em_outras_lojas = produto.url_set.all().exclude(loja__id=loja_id)

        prods = {
            'nome': produto.nome,
            'meu_preco': float(produto.preco),
            'disponibilidade': produto.disponibilidade,
            'codigo': produto.codigo,
            'urls': [{
                'endereco': url.endereco,
                'preco': float(url.produto.preco)
            } for url in urls_deste_produto_em_outras_lojas]
        }

        produtos.append(prods)

    return HttpResponse(json.dumps({
        'produtos': produtos
    }))


@require_http_methods(['POST'])
def criar(request, tipo):

    form_class, _ = get_model_e_form_por_tipo(tipo)

    if not form_class:
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


@require_http_methods(['PUT'])
def atualizar(request, tipo, pk):

    form_class, model_class = get_model_e_form_por_tipo(tipo)

    if not form_class:
        raise Http404()

    values = dict(parse_qsl(request.body))

    model_instance = get_object_or_404(model_class, pk=pk)

    for key, value in values.items():
        setattr(model_instance, key, value)

    form = form_class(model_to_dict(model_instance))

    response = HttpResponse()

    if form.is_valid():
        model_instance.save()
        response.status_code = 204
    else:
        response.status_code = 400

    return response


@require_http_methods(['DELETE'])
def remover(request, tipo, pk):

    _, model_class = get_model_e_form_por_tipo(tipo)

    if not model_class:
        raise Http404()

    model_instance = get_object_or_404(model_class, pk=pk)
    model_instance.delete()

    return HttpResponse()


def get_model_e_form_por_tipo(tipo):
    if tipo == 'loja':
        model_class = Loja
        form_class = LojaForm
    elif tipo == 'produto':
        model_class = Produto
        form_class = ProdutoForm
    elif tipo == 'cliente':
        model_class = Cliente
        form_class = ClienteForm
    elif tipo == 'url':
        model_class = Url
        form_class = UrlForm
    else:
        return None, None

    return form_class, model_class
