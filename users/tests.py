from django.contrib.auth.models import User
from django.test import TestCase, override_settings


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class AlterarSenhaTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='aluno', password='velha-123')

    def test_requer_login(self):
        resp = self.client.get('/alterar-senha/')
        self.assertEqual(resp.status_code, 302)

    def test_pagina_renderiza_form(self):
        self.client.force_login(self.user)
        resp = self.client.get('/alterar-senha/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Alterar senha')

    def test_troca_senha_com_sucesso(self):
        self.client.force_login(self.user)
        resp = self.client.post('/alterar-senha/', {
            'old_password': 'velha-123',
            'new_password1': 'nova-456!',
            'new_password2': 'nova-456!',
        })
        self.assertRedirects(resp, '/dashboard/')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('nova-456!'))

    def test_senha_atual_errada_nao_altera(self):
        self.client.force_login(self.user)
        resp = self.client.post('/alterar-senha/', {
            'old_password': 'errada',
            'new_password1': 'nova-456!',
            'new_password2': 'nova-456!',
        })
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('velha-123'))
        self.assertTrue(resp.context['form'].errors)

    def test_confirmacao_divergente_nao_altera(self):
        self.client.force_login(self.user)
        resp = self.client.post('/alterar-senha/', {
            'old_password': 'velha-123',
            'new_password1': 'nova-456!',
            'new_password2': 'diferente!',
        })
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('velha-123'))