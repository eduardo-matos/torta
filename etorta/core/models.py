from django.db import models


class Loja(models.Model):
    nome = models.CharField()

    class Meta:
        db_table = 'loja'


class Cliente(models.Model):
    nome = models.CharField()
    loja = models.ForeignKey('Loja')

    class Meta:
        db_table = 'cliente'


class Produto(models.Model):
    nome = models.CharField()
    disponibilidade = models.BooleanField()
    codigo = models.IntegerField()
    meu_preco = models.DecimalField()
    loja = models.ForeignKey('Loja')

    class Meta:
        db_table = 'produto'


class Url(models.Model):
    endereco = models.CharField()
    disponibilidade = models.BooleanField()
    preco = models.DecimalField()
    loja = models.ForeignKey('Loja')
    produto = models.ForeignKey('Produto')

    class Meta:
        db_table = 'url'
