# coding: utf-8

from django.test import TestCase
from django.core.urlresolvers import reverse as r, reverse_lazy as rl
from django.contrib.auth import get_user_model

User = get_user_model()

class TestLogin(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')

    def test_login_page_has_password_field(self):
        resp = self.client.get(r('core:login'))
        self.assertContains(resp, 'type="password"')

    def test_consegue_logar_com_credenciais_certas(self):
        resp = self.client.post(r('core:login'), {'username': 'edu', 'password': 'edu'})
        self.assertEqual(302, resp.status_code)

    def test_nao_consegue_logar_com_credenciais_erradas(self):
        resp = self.client.post(r('core:login'), {'username': 'a', 'password': 'b'})
        self.assertEqual(200, resp.status_code)

    def test_exibe_mensagem_de_erro_se_nao_conseguir_logar(self):
        resp = self.client.post(r('core:login'), {'username': 'a', 'password': 'b'})
        self.assertContains(resp, 'Usuário não encontrado')

    def test_redireciona_para_url_correta_se_next_for_passado(self):
        resp = self.client.post(r('core:login'), {'username': 'edu', 'password': 'edu', 'next': rl('core:home')}, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'Seja bem vindo ao eTorta!')


class TestLogout(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='edu', password='edu')

    def test_consegue_fazer_logout(self):
        self.client.post(r('core:login'), {'username': 'edu', 'password': 'edu'})
        resp = self.client.get(r('core:logout'), follow=True)
        self.assertEqual(200, resp.status_code)
