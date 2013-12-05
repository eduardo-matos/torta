from django.db import models
from django.contrib.auth import get_user_model


class Loja(models.Model):
    nome = models.CharField(max_length=100)
    produtos = models.ManyToManyField('Produto', through='Url')
    dono = models.ForeignKey(get_user_model())

    def __unicode__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    disponibilidade = models.BooleanField(default=False)
    codigo = models.IntegerField()
    preco = models.DecimalField(decimal_places=2, max_digits=10)

    def __unicode__(self):
        return self.nome


class Url(models.Model):
    endereco = models.CharField(max_length=100)
    disponibilidade = models.BooleanField(default=False)
    loja = models.ForeignKey('Loja')
    produto = models.ForeignKey('Produto')

    def __unicode__(self):
        return self.endereco
