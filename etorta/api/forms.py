# coding: utf-8

from django import forms
from core.models import Loja, Produto, Cliente, Url


class LojaForm(forms.ModelForm):

    class Meta:
        model = Loja
        fields = ('nome',)


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ('nome', 'disponibilidade', 'codigo', 'preco',)


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('nome', 'loja',)


class UrlForm(forms.ModelForm):

    class Meta:
        model = Url
        fields = ('endereco', 'disponibilidade', 'loja', 'produto',)
