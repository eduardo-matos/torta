from django.test import TestCase
from core.models import Loja, Cliente, Produto, Url
from django.core.urlresolvers import reverse as r
from model_mommy import mommy
import json

# Create your tests here.
class TestApiGet(TestCase):
    
    def setUp(self):
        self.minha_loja = mommy.make(Loja)

    def test_status(self):
        resp = self.client.get(r('api:get', kwargs={'loja_id': self.minha_loja.pk}))
        self.assertEqual(200, resp.status_code)

    def test_status_404_se_id_loja_nao_for_passado(self):
        resp = self.client.get(r('api:get'))
        self.assertEqual(404, resp.status_code)

    def test_retorna_lista_de_produtos_de_uma_loja(self):
        produto = mommy.make(Produto, loja = self.minha_loja, _quantity=2)
        mommy.make(Url, _quantity=10)

        resp = self.client.get(r('api:get', kwargs={'loja_id': self.minha_loja.pk}))
        self.assertEqual(2, len(json.loads(resp.content)['produtos']))

    def test_retorna_informacoes_de_outras_lojas(self):
        produto = mommy.make(Produto, loja = self.minha_loja, _quantity=2)
        lojas = mommy.make(Url, _quantity=10)

        resp = self.client.get(r('api:get', kwargs={'loja_id': self.minha_loja.pk}))
        self.assertTrue(len(json.loads(resp.content)['produtos'][0]['urls']) >= 1)
