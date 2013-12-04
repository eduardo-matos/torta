from django.shortcuts import render
from django.http import HttpResponse
from core.models import Produto, Url, Loja
from django.shortcuts import get_object_or_404
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
