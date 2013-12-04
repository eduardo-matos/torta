from django.test import TestCase
from core.models import Loja, Cliente, Produto, Url
from django.core.urlresolvers import reverse as r
import urllib
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


class TestApiCriar(TestCase):

    def test_salvar_model(self):
        # salvar Loja
        resp = self.client.post(r('api:criar', args=('loja',)), {'nome': 'test'})
        self.assertEqual(201, resp.status_code)
        self.assertTrue(Loja.objects.exists())

        # salvar Produto
        resp = self.client.post(r('api:criar', args=('produto',)), {
            'nome': 'test',
            'disponibilidade': True,
            'codigo': 123,
            'meu_preco': 10.7,
            'loja': 1
        })
        self.assertEqual(201, resp.status_code)
        self.assertTrue(Produto.objects.exists())

        #salvar Cliente
        resp = self.client.post(r('api:criar', args=('cliente',)), {
            'nome': 'test',
            'loja': 1
        })
        self.assertEqual(201, resp.status_code)
        self.assertTrue(Cliente.objects.exists())

        #salvar Url
        resp = self.client.post(r('api:criar', args=('url',)), {
            'endereco': '/a/b',
            'disponibilidade': False,
            'preco': 14.3,
            'loja': 1,
            'produto': 1
        })
        self.assertEqual(201, resp.status_code)
        self.assertTrue(Url.objects.exists())

    def test_deve_retornar_status_400_e_lista_erros_se_nao_conseguir_salvar_model(self):
        resp = self.client.post(r('api:criar', args=('loja',)), dict())
        self.assertEqual(400, resp.status_code)
        self.assertTrue('nome' in json.loads(resp.content))
        self.assertFalse(Loja.objects.exists())

    def test_status_404_se_tentar_salvar_model_que_nao_existe(self):
        resp = self.client.post(r('api:criar', args=('dummy',)), {'a': 'b'})
        self.assertEqual(404, resp.status_code)


class TestApiAtualizar(TestCase):

    def setUp(self):
        self.loja = mommy.make(Loja)
        self.produto = mommy.make(Produto)
        self.cliente = mommy.make(Cliente)
        self.url = mommy.make(Url)

    def test_atualizar_models(self):
        # salvar Loja
        resp = self.client.put(r('api:atualizar', args=('loja', self.loja.pk,)), urllib.urlencode({'nome': 'aaa'}))
        self.assertEqual(204, resp.status_code)
        self.assertEqual('aaa', Loja.objects.get(pk=self.loja.pk).nome)

        # salvar Produto
        resp = self.client.put(r('api:atualizar', args=('produto', self.produto.pk,)), urllib.urlencode({'nome': 'bbb', 'meu_preco': 10, 'codigo': 10}))
        self.assertEqual(204, resp.status_code)
        self.assertEqual('bbb', Produto.objects.get(pk=self.produto.pk).nome)
        self.assertEqual(10, Produto.objects.get(pk=self.produto.pk).meu_preco)
        self.assertEqual(10, Produto.objects.get(pk=self.produto.pk).codigo)

        # salvar Cliente
        resp = self.client.put(r('api:atualizar', args=('cliente', self.cliente.pk,)), urllib.urlencode({'nome': 'ccc'}))
        self.assertEqual(204, resp.status_code)
        self.assertEqual('ccc', Cliente.objects.get(pk=self.cliente.pk).nome)

        # salvar Url
        resp = self.client.put(r('api:atualizar', args=('url', self.url.pk,)), urllib.urlencode({'endereco': 'ccc', 'preco': 2}))
        self.assertEqual(204, resp.status_code)
        self.assertEqual('ccc', Url.objects.get(pk=self.url.pk).endereco)
        self.assertEqual(2, Url.objects.get(pk=self.url.pk).preco)

    def test_status_404_se_tentar_salvar_model_que_nao_existe(self):
        resp = self.client.put(r('api:atualizar', args=('dummy', self.url.pk,)), urllib.urlencode({'endereco': 'ccc', 'preco': 2}))
        self.assertEqual(404, resp.status_code)

    def test_status_404_quando_tenta_atualizar_model_que_nao_existe(self):
        resp = self.client.put(r('api:atualizar', args=('loja', 50,)), urllib.urlencode({'endereco': 'ccc', 'preco': 2}))
        self.assertEqual(404, resp.status_code)

    def test_status_400_quando_os_dados_nao_validam(self):
        resp = self.client.put(r('api:atualizar', args=('loja', self.loja.pk,)), urllib.urlencode({'nome': 'x' * 200}))
        self.assertEqual(400, resp.status_code)
