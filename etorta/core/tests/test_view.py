from django.test import TestCase
from django.core.urlresolvers import reverse as r
from core.models import Produto, Loja, Url, Cliente
from model_mommy import mommy
from django.forms.models import model_to_dict


class TestViewProdutos(TestCase):

    def setUp(self):
        self.resp = self.client.get(r('core:produtos'))

    def test_retorna_status_200(self):
        self.assertEqual(200, self.resp.status_code)

    def test_home_exibe_lista_de_produtos(self):
        self.assertContains(self.resp, 'class="lista-produtos"')


class TestViewCriarModel(TestCase):

    def test_retorna_status_200(self):
        resp = self.client.post(r('core:model-criar', kwargs={'tipo': 'loja'}))
        self.assertEqual(200, resp.status_code)

        resp = self.client.post(r('core:model-criar', kwargs={'tipo': 'produto'}))
        self.assertEqual(200, resp.status_code)

        resp = self.client.post(r('core:model-criar', kwargs={'tipo': 'cliente'}))
        self.assertEqual(200, resp.status_code)

        resp = self.client.post(r('core:model-criar', kwargs={'tipo': 'url'}))
        self.assertEqual(200, resp.status_code)

    def test_permite_salvar_models(self):
        # salvar Loja
        resp = self.client.post(r('core:model-criar', kwargs={'tipo': 'loja'}), {'nome': 'Americanas',})
        self.assertTrue(Loja.objects.exists())

        # salvar Produto
        resp = self.client.post(r('core:model-criar', kwargs={'tipo': 'produto'}), {'nome': 'Biscoito', 'codigo': 1, 'preco': 10})
        self.assertTrue(Produto.objects.exists())

        # salvar  Cliente
        loja = mommy.make(Loja)
        resp = self.client.post(r('core:model-criar', kwargs={'tipo': 'cliente'}), {'nome': 'Dummy', 'loja': loja.pk})
        self.assertTrue(Cliente.objects.exists())

        # salvar Url
        produto = mommy.make(Produto)
        loja = mommy.make(Loja)
        resp = self.client.post(r('core:model-criar', kwargs={'tipo': 'url'}),
            {'endereco': '/a/b', 'disponibilidade': True, 'loja': loja.pk, 'produto': produto.pk})
        self.assertTrue(Url.objects.exists())


class TestViewAtualizaModel(TestCase):

    def setUp(self):
        self.loja = mommy.make(Loja)
        self.produto = mommy.make(Produto)
        self.cliente = mommy.make(Cliente)
        self.url = mommy.make(Url)

    def test_retorna_status_200(self):

        resp_loja = self.client.get(r('core:model-atualizar', kwargs={'tipo': 'loja', 'pk': self.loja.pk,}))
        resp_produto = self.client.get(r('core:model-atualizar', kwargs={'tipo': 'produto', 'pk': self.produto.pk,}))
        resp_cliente = self.client.get(r('core:model-atualizar', kwargs={'tipo': 'cliente', 'pk': self.cliente.pk,}))
        resp_url = self.client.get(r('core:model-atualizar', kwargs={'tipo': 'url', 'pk': self.url.pk,}))

        self.assertEqual(200, resp_loja.status_code)
        self.assertEqual(200, resp_produto.status_code)
        self.assertEqual(200, resp_cliente.status_code)
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

        cliente_props = model_to_dict(self.cliente)
        cliente_props.update({'nome': 'Ccc'})
        resp = self.client.post(r('core:model-atualizar', kwargs={'tipo': 'cliente', 'pk': self.cliente.pk,}), cliente_props)
        cliente = Cliente.objects.get(pk=self.cliente.pk)
        self.assertEqual('Ccc', cliente.nome)

        url_props = model_to_dict(self.url)
        url_props.update({'endereco': 'Ddd'})
        resp = self.client.post(r('core:model-atualizar', kwargs={'tipo': 'url', 'pk': self.url.pk,}), url_props)
        url = Url.objects.get(pk=self.url.pk)
        self.assertEqual('Ddd', url.endereco)


class TestViewRemoverModel(TestCase):

    def setUp(self):
        self.loja = mommy.make(Loja)
        self.produto = mommy.make(Produto)
        self.cliente = mommy.make(Cliente)
        self.url = mommy.make(Url)

    def test_retorna_status_200(self):
        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'loja', 'pk': self.loja.pk,}))
        self.assertEqual(200, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'produto', 'pk': self.produto.pk,}))
        self.assertEqual(200, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'cliente', 'pk': self.cliente.pk,}))
        self.assertEqual(200, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'url', 'pk': self.url.pk,}))
        self.assertEqual(200, resp.status_code)

    def test_remocao_model(self):
        self.resp = self.client.post(r('core:model-remover', kwargs={'tipo': 'loja', 'pk': self.loja.pk,}))
        self.assertRaises(Loja.objects.get, pk=self.loja.pk)

        self.resp = self.client.post(r('core:model-remover', kwargs={'tipo': 'produto', 'pk': self.produto.pk,}))
        self.assertRaises(Produto.objects.get, pk=self.produto.pk)

        self.resp = self.client.post(r('core:model-remover', kwargs={'tipo': 'cliente', 'pk': self.cliente.pk,}))
        self.assertRaises(Cliente.objects.get, pk=self.cliente.pk)

        self.resp = self.client.post(r('core:model-remover', kwargs={'tipo': 'url', 'pk': self.url.pk,}))
        self.assertRaises(Url.objects.get, pk=self.url.pk)

    def test_retorna_status_404_quando_model_nao_eh_encontrado(self):
        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'loja', 'pk': 97,}))
        self.assertEqual(404, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'produto', 'pk': 97,}))
        self.assertEqual(404, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'cliente', 'pk': 97,}))
        self.assertEqual(404, resp.status_code)

        resp = self.client.get(r('core:model-remover', kwargs={'tipo': 'url', 'pk': 97,}))
        self.assertEqual(404, resp.status_code)


class TestHome(TestCase):

    def test_home_exists(self):
        resp = self.client.get(r('core:home'))
        self.assertEqual(200, resp.status_code)
