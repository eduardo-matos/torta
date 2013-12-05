from django.test import TestCase
from django.core.urlresolvers import reverse as r


class TestViewProdutos(TestCase):

    def setUp(self):
        self.resp = self.client.get(r('core:produtos'))

    def test_retorna_status_200(self):
        self.assertEqual(200, self.resp.status_code)

    def test_home_exibe_lista_de_produtos(self):
        self.assertContains(self.resp, 'class="lista-produtos"')
