from django.test import TestCase
from django.core.urlresolvers import reverse as r
from core.models import Produto
from model_mommy import mommy


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


class TestViewAtualizaProduto(TestCase):

    def setUp(self):
        self.produto = mommy.make(Produto)
        self.resp = self.client.get(r('core:produto-atualizar', kwargs={'pk': self.produto.pk,}))

    def test_retorna_status_200(self):
        self.assertEqual(200, self.resp.status_code)

    def test_campos_do_formulario_existem(self):
        self.assertContains(self.resp, '<input ', 6)

    def test_atualizar_produto(self):
        resp = self.client.post(r('core:produto-atualizar', kwargs={'pk': self.produto.pk,}), {'nome': 'Biscoito', 'codigo': 1, 'preco': 10})
        produto = Produto.objects.get(pk=self.produto.pk)
        self.assertEqual('Biscoito', produto.nome)
        self.assertEqual(1, produto.codigo)
        self.assertEqual(10, produto.preco)

    def test_campos_aparecem_preenchidos(self):
        resp = self.client.get(r('core:produto-atualizar', kwargs={'pk': self.produto.pk,}))
        self.assertContains(resp, ''.join(['value="', self.produto.nome, '"']))
        self.assertContains(resp, ''.join(['value="', str(self.produto.codigo), '"']))
        self.assertContains(resp, ''.join(['value="', str(self.produto.preco), '"']))


class TestViewRemoverProduto(TestCase):

    def setUp(self):
        self.produto = mommy.make(Produto)

    def test_retorna_status_200(self):
        resp = self.client.get(r('core:produto-remover', kwargs={'pk': self.produto.pk,}))
        self.assertEqual(200, resp.status_code)

    def test_remocao_produto(self):
        self.resp = self.client.post(r('core:produto-remover', kwargs={'pk': self.produto.pk,}))
        self.assertFalse(Produto.objects.exists())

    def test_retorna_status_404_quando_produto_nao_eh_encontrado(self):
        resp = self.client.get(r('core:produto-remover', kwargs={'pk': 97,}))
        self.assertEqual(404, resp.status_code)
