from django.test import TestCase
from django.core.urlresolvers import reverse as r
from core.models import Produto


class TestViewProdutos(TestCase):

    def setUp(self):
        self.resp = self.client.get(r('core:produtos'))

    def test_retorna_status_200(self):
        self.assertEqual(200, self.resp.status_code)

    def test_home_exibe_lista_de_produtos(self):
        self.assertContains(self.resp, 'class="lista-produtos"')


class TestViewCriarProdutos(TestCase):

    def setUp(self):
        self.resp = self.client.get(r('core:produto-criar'))

    def test_retorna_status_200(self):
        self.assertEqual(200, self.resp.status_code)

    def test_home_exibe_lista_de_produtos(self):
        self.assertContains(self.resp, '<input ', 6)

    def test_permite_salvar_produto(self):
        resp = self.client.post(r('core:produto-criar'), {'nome': 'Biscoito', 'codigo': 1, 'preco': 10})
        self.assertTrue(Produto.objects.exists())
