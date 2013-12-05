from django.test import TestCase
from core.models import Loja, Produto, Url
from django.core.urlresolvers import reverse as r
import urllib
from model_mommy import mommy
import json
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class TestApiGet(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')
        self.client.login(username='edu', password='edu')
        self.minha_loja = mommy.make(Loja, dono=self.user)

    def test_status(self):
        resp = self.client.get(r('api:get', kwargs={'loja_id': self.minha_loja.pk}))
        self.assertEqual(200, resp.status_code)

    def test_status_404_se_usuario_tentar_acessar_loja_que_nao_lhe_pertence(self):
        loja = mommy.make(Loja)
        resp = self.client.get(r('api:get', kwargs={'loja_id': loja.pk}))
        self.assertEqual(404, resp.status_code)

    def test_status_404_se_id_loja_nao_for_passado(self):
        resp = self.client.get(r('api:get'))
        self.assertEqual(404, resp.status_code)

    def test_retorna_lista_de_produtos_de_uma_loja(self):
        produto1 = mommy.make(Produto)
        produto2 = mommy.make(Produto)
        loja1 = mommy.make(Loja)
        loja2 = self.minha_loja

        url1 = mommy.make(Url, loja=loja1, produto=produto1)
        url2 = mommy.make(Url, loja=loja1, produto=produto2)
        url3 = mommy.make(Url, loja=loja2, produto=produto1)

        resp = self.client.get(r('api:get', kwargs={'loja_id': loja2.pk}))
        self.assertEqual(1, len(json.loads(resp.content)['produtos']))

    def test_retorna_informacoes_de_outras_lojas(self):
        produto1 = mommy.make(Produto)
        produto2 = mommy.make(Produto)
        loja1 = self.minha_loja
        loja2 = mommy.make(Loja)
        loja3 = mommy.make(Loja)

        url1 = mommy.make(Url, loja=loja1, produto=produto1)
        url2 = mommy.make(Url, loja=loja2, produto=produto1)
        url3 = mommy.make(Url, loja=loja3, produto=produto1)

        resp = self.client.get(r('api:get', kwargs={'loja_id': loja1.pk}))
        self.assertEqual(2, len(json.loads(resp.content)['produtos'][0]['urls']))


class TestApiCriar(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')
        self.client.login(username='edu', password='edu')

    def test_salvar_model(self):
        # salvar Loja
        resp = self.client.post(r('api:criar', args=('loja',)), {'nome': 'test'})
        self.assertEqual(201, resp.status_code)
        self.assertEqual(Loja.objects.get(pk=1).dono, self.user)

        # salvar Produto
        resp = self.client.post(r('api:criar', args=('produto',)), {
            'nome': 'test',
            'disponibilidade': True,
            'codigo': 123,
            'preco': 10.7,
            'loja': 1
        })
        self.assertEqual(201, resp.status_code)
        self.assertTrue(Produto.objects.exists())

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
        self.user = User.objects.create_user(username='edu', password='edu')
        self.client.login(username='edu', password='edu')

        self.loja = mommy.make(Loja, dono=self.user)
        self.produto = mommy.make(Produto)
        self.url = mommy.make(Url)

    def test_atualizar_models(self):
        # salvar Loja
        resp = self.client.put(r('api:atualizar', args=('loja', self.loja.pk,)), urllib.urlencode({'nome': 'aaa'}))
        self.assertEqual(204, resp.status_code)
        self.assertEqual('aaa', Loja.objects.get(pk=self.loja.pk).nome)

        # salvar Produto
        resp = self.client.put(r('api:atualizar', args=('produto', self.produto.pk,)), urllib.urlencode({'nome': 'bbb', 'preco': 10, 'codigo': 10}))
        self.assertEqual(204, resp.status_code)
        self.assertEqual('bbb', Produto.objects.get(pk=self.produto.pk).nome)
        self.assertEqual(10, Produto.objects.get(pk=self.produto.pk).preco)
        self.assertEqual(10, Produto.objects.get(pk=self.produto.pk).codigo)

        # salvar Url
        resp = self.client.put(r('api:atualizar', args=('url', self.url.pk,)), urllib.urlencode({'endereco': 'ccc', 'preco': 2}))
        self.assertEqual(204, resp.status_code)
        self.assertEqual('ccc', Url.objects.get(pk=self.url.pk).endereco)

    def test_status_404_se_tentar_salvar_model_que_nao_existe(self):
        resp = self.client.put(r('api:atualizar', args=('dummy', self.url.pk,)), urllib.urlencode({'endereco': 'ccc', 'preco': 2}))
        self.assertEqual(404, resp.status_code)

    def test_status_404_quando_tenta_atualizar_model_que_nao_existe(self):
        resp = self.client.put(r('api:atualizar', args=('loja', 50,)), urllib.urlencode({'endereco': 'ccc', 'preco': 2}))
        self.assertEqual(404, resp.status_code)

    def test_status_400_quando_os_dados_nao_validam(self):
        resp = self.client.put(r('api:atualizar', args=('loja', self.loja.pk,)), urllib.urlencode({'nome': 'x' * 200}))
        self.assertEqual(400, resp.status_code)


class TestApiRemover(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')
        self.client.login(username='edu', password='edu')

        self.loja = mommy.make(Loja, dono=self.user)
        self.produto = mommy.make(Produto)

    def test_remover_models(self):
        # remover Loja
        resp = self.client.delete(r('api:remover', args=('loja', self.loja.pk,)))
        self.assertEqual(200, resp.status_code)
        self.assertRaises(Loja.objects.get, pk=self.loja.pk)

        # remover Produto
        resp = self.client.delete(r('api:remover', args=('produto', self.produto.pk,)))
        self.assertEqual(200, resp.status_code)
        self.assertRaises(Produto.objects.get, pk=self.produto.pk)

    def test_status_404_quando_nao_encontra_model(self):
        resp = self.client.delete(r('api:remover', args=('dummy', 1,)))
        self.assertEqual(404, resp.status_code)

    def test_status_404_quando_nao_encontra_model_no_banco_de_dados(self):
        resp = self.client.delete(r('api:remover', args=('produto', 9845,)))
        self.assertEqual(404, resp.status_code)
