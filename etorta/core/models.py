from django.db import models


class Loja(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    loja = models.ForeignKey('Loja')

    def __unicode__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    disponibilidade = models.BooleanField(default=False)
    codigo = models.IntegerField()
    meu_preco = models.DecimalField(decimal_places=2, max_digits=10)
    loja = models.ForeignKey('Loja')

    def __unicode__(self):
        return self.nome


class Url(models.Model):
    endereco = models.CharField(max_length=100)
    disponibilidade = models.BooleanField(default=False)
    preco = models.DecimalField(decimal_places=2, max_digits=10)
    loja = models.ForeignKey('Loja')
    produto = models.ForeignKey('Produto')

    def __unicode__(self):
        return self.endereco
