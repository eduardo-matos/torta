from django.test import TestCase
from django.core.urlresolvers import reverse as r
from core.models import Produto, Loja, Url
from model_mommy import mommy
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

User = get_user_model()

class TestViewProdutos(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')
        self.client.login(username='edu', password='edu')
        self.resp = self.client.get(r('core:produtos'))

    def test_retorna_status_200(self):
        self.assertEqual(200, self.resp.status_code)

    def test_home_exibe_lista_de_produtos(self):
        self.assertContains(self.resp, 'class="lista-produtos"')


class TestViewLojaCriar(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')
        self.client.login(username='edu', password='edu')

    def test_retorna_status_200(self):
        resp = self.client.post(r('core:loja-criar'))
        self.assertEqual(200, resp.status_code)

    def test_permite_salvar_models(self):
        # salvar Loja
        resp = self.client.post(r('core:loja-criar'), {'nome': 'Abc'})
        self.assertTrue(Loja.objects.exists())


class TestViewCriarProduto(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')
        self.client.login(username='edu', password='edu')

    def test_pagina_exists(self):
        resp = self.client.get(r('core:produto-criar'))
        self.assertEqual(200, resp.status_code)

    def test_consegue_criar_produto_com_informacoes_corretas(self):
        loja = mommy.make(Loja, dono=self.user)
        resp = self.client.post(r('core:produto-criar'), {
            'produto-nome': 'abc',
            'produto-codigo': '123',
            'produto-preco': '10.2',
            'url-endereco': '/a/b/c',
            'url-disponibilidade': True,
            'url-loja': loja.pk,
            'url-produto': ''
        })
        self.assertEqual(302, resp.status_code)
        self.assertEqual(1, loja.produtos.count())

    def test_nao_consegue_salvar_produto_com_informacoes_erradas(self):
        loja = mommy.make(Loja, dono=self.user)
        resp = self.client.post(r('core:produto-criar'), {
            'produto-nome': '',
            'produto-preco': '10.2',
            'url-endereco': '/a/b/c',
            'url-produto': ''
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(0, loja.produtos.count())
        self.assertContains(resp, 'error')

    def test_redireciona_para_pagina_de_produtos_ao_salvar(self):
        loja = mommy.make(Loja, dono=self.user)
        resp = self.client.post(r('core:produto-criar'), {
            'produto-nome': 'abc',
            'produto-codigo': '123',
            'produto-preco': '10.2',
            'url-endereco': '/a/b/c',
            'url-disponibilidade': True,
            'url-loja': loja.pk,
            'url-produto': ''
        }, follow=True)
        self.assertContains(resp, 'info-produto')


class TestViewAtualizaModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')
        self.client.login(username='edu', password='edu')

        self.loja = mommy.make(Loja, dono=self.user)
        self.produto = mommy.make(Produto)
        self.url = mommy.make(Url)

    def test_retorna_status_200(self):

        resp_loja = self.client.get(r('core:model-atualizar', kwargs={'tipo': 'loja', 'pk': self.loja.pk,}))
        resp_produto = self.client.get(r('core:model-atualizar', kwargs={'tipo': 'produto', 'pk': self.produto.pk,}))
        resp_url = self.client.get(r('core:model-atualizar', kwargs={'tipo': 'url', 'pk': self.url.pk,}))

        self.assertEqual(200, resp_loja.status_code)
        self.assertEqual(200, resp_produto.status_code)
        self.assertEqual(200, resp_url.status_code)

    def test_atualizar_model(self):

        loja_props = model_to_dict(self.loja)
        loja_props.update({'nome': 'Aaa'})
        resp = self.client.post(r('core:model-atualizar', kwargs={'tipo': 'loja', 'pk': self.loja.pk,}), loja_props)
        loja = Loja.objects.get(pk=self.loja.pk)
        self.assertEqual('Aaa', loja.nome)

        produto_props = model_to_dict(self.produto)
        produto_props.update({'nome': 'Bbb'})
        resp = self.client.post(r('core:model-atualizar', kwargs={'tipo': 'produto', 'pk': self.produto.pk,}), produto_props)
        produto = Produto.objects.get(pk=self.produto.pk)
        self.assertEqual('Bbb', produto.nome)

        url_props = model_to_dict(self.url)
        url_props.update({'endereco': 'Ddd'})
        resp = self.client.post(r('core:model-atualizar', kwargs={'tipo': 'url', 'pk': self.url.pk,}), url_props)
        url = Url.objects.get(pk=self.url.pk)
        self.assertEqual('Ddd', url.endereco)

    def test_status_404_se_usuario_nao_eh_dono_da_loja(self):
        dummy_user = User.objects.create_user(username='a', password='a')
        loja = mommy.make(Loja, dono=dummy_user)
        loja_props = model_to_dict(loja)
        loja_props.update({'nome': 'Aaa'})
        resp = self.client.post(r('core:model-atualizar', kwargs={'tipo': 'loja', 'pk': loja.pk,}), loja_props)
        self.assertEqual(404, resp.status_code)


class TestViewRemoverModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')
        self.client.login(username='edu', password='edu')

        self.loja = mommy.make(Loja)
        self.produto = mommy.make(Produto)
        self.url = mommy.make(Url)

    def test_retorna_status_200(self):
        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'loja', 'pk': self.loja.pk,}))
        self.assertEqual(200, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'produto', 'pk': self.produto.pk,}))
        self.assertEqual(200, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'url', 'pk': self.url.pk,}))
        self.assertEqual(200, resp.status_code)

    def test_remocao_model(self):
        self.resp = self.client.post(r('core:model-remover', kwargs={'tipo': 'loja', 'pk': self.loja.pk,}))
        self.assertRaises(Loja.objects.get, pk=self.loja.pk)

        self.resp = self.client.post(r('core:model-remover', kwargs={'tipo': 'produto', 'pk': self.produto.pk,}))
        self.assertRaises(Produto.objects.get, pk=self.produto.pk)

        self.resp = self.client.post(r('core:model-remover', kwargs={'tipo': 'url', 'pk': self.url.pk,}))
        self.assertRaises(Url.objects.get, pk=self.url.pk)

    def test_retorna_status_404_quando_model_nao_eh_encontrado(self):
        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'loja', 'pk': 97,}))
        self.assertEqual(404, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'produto', 'pk': 97,}))
        self.assertEqual(404, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'url', 'pk': 97,}))
        self.assertEqual(404, resp.status_code)


class TestHome(TestCase):

    def test_home_exists(self):
        resp = self.client.get(r('core:home'))
        self.assertEqual(200, resp.status_code)
