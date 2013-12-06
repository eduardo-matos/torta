# coding: utf-8

from django import forms
from core.models import Loja, Produto, Url


class LojaForm(forms.ModelForm):

    class Meta:
        model = Loja
        fields = ('nome',)


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ('nome', 'codigo', 'preco',)


class UrlForm(forms.ModelForm):

    class Meta:
        model = Url
        fields = ('endereco', 'disponibilidade', 'loja', 'produto',)


class UrlFormCriarProduto(forms.ModelForm):

    class Meta:
        model = Url
        fields = ('endereco', 'disponibilidade', 'loja',)
