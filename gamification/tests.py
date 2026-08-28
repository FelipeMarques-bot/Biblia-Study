# -*- coding: utf-8 -*-
from datetime import date, datetime, time

from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from .leagues import inicio_semana, calcular_ligas
from .models import Liga, LigaParticipacao, UserActivityLog

SEMANA_A = date(2026, 1, 5)    # segunda
SEMANA_B = date(2026, 1, 12)   # segunda seguinte


def _log(usuario, xp, quando):
    log = UserActivityLog.objects.create(
        usuario=usuario,
        tipo_atividade='LICAO_CONCLUIDA',
        descricao_resumida='teste',
        xp_ganho=xp,
    )
    UserActivityLog.objects.filter(pk=log.pk).update(
        data_hora=quando
    )
    return log


def _usuario(username):
    u = User.objects.create_user(username=username, password='x')
    u.profile.xp_total = 0
    u.profile.save()
    return u


def _parts(usuario, semana):
    return LigaParticipacao.objects.get(usuario=usuario, semana=semana)


class LigaSeedTest(TestCase):

    def test_ligas_seedadas(self):
        ligas = list(Liga.objects.order_by('ordem'))
        self.assertEqual(len(ligas), 10)
        nomes = [l.nome for l in ligas]
        self.assertEqual(nomes[0], 'Bronze')
        self.assertEqual(nomes[-1], 'Diamante')
        self.assertIn('metal', {l.tipo for l in ligas})
        self.assertIn('pedra', {l.tipo for l in ligas})

    def test_inicio_semana(self):
        self.assertEqual(inicio_semana(date(2026, 1, 8)), SEMANA_A)


class CalcularLigasTest(TestCase):

    def test_primeira_semana_coloca_novos_no_bronze(self):
        u1 = _usuario('u1')
        u2 = _usuario('u2')
        _log(u1, 100, datetime.combine(SEMANA_A, time(10)))
        _log(u2, 50, datetime.combine(SEMANA_A, time(11)))

        calcular_ligas(semana=SEMANA_A)

        bronze = Liga.objects.get(ordem=1)
        prata = Liga.objects.get(ordem=2)
        p1 = _parts(u1, SEMANA_A)
        p2 = _parts(u2, SEMANA_A)
        # melhor da semana sobe; o seguinte permanece no bronze
        self.assertEqual(p1.liga_id, prata.id)
        self.assertTrue(p1.promovido)
        self.assertEqual(p1.liga_anterior_id, bronze.id)
        self.assertEqual(p2.liga_id, bronze.id)
        self.assertFalse(p2.promovido)
        self.assertEqual(p2.posicao, 1)
        self.assertEqual(p2.xp_semana, 50)

    def test_movimenta_entre_ligas(self):
        # Semana A: u1 e u2 (os 2 melhores do bronze) sobem para a prata
        u1 = _usuario('u1')
        u2 = _usuario('u2')
        u3 = _usuario('u3')
        u4 = _usuario('u4')
        _log(u1, 100, datetime.combine(SEMANA_A, time(10)))
        _log(u2, 80, datetime.combine(SEMANA_A, time(11)))
        _log(u3, 10, datetime.combine(SEMANA_A, time(12)))
        _log(u4, 60, datetime.combine(SEMANA_A, time(13)))

        calcular_ligas(semana=SEMANA_A)

        bronze = Liga.objects.get(ordem=1)
        prata = Liga.objects.get(ordem=2)
        p1 = _parts(u1, SEMANA_A)
        p2 = _parts(u2, SEMANA_A)
        p3 = _parts(u3, SEMANA_A)
        p4 = _parts(u4, SEMANA_A)
        self.assertEqual(p1.liga_id, prata.id)
        self.assertEqual(p2.liga_id, prata.id)
        self.assertEqual(p3.liga_id, bronze.id)
        self.assertEqual(p4.liga_id, bronze.id)
        self.assertTrue(p1.promovido)
        self.assertEqual(p1.posicao, 1)
        self.assertEqual(p2.posicao, 2)

        # Semana B: u3 avança; u2 (inativo no fundo da prata) cai; u5 estreia
        u5 = _usuario('u5')
        _log(u3, 120, datetime.combine(SEMANA_B, time(10)))
        _log(u4, 90, datetime.combine(SEMANA_B, time(11)))
        _log(u5, 5, datetime.combine(SEMANA_B, time(12)))

        calcular_ligas(semana=SEMANA_B)

        b1 = _parts(u1, SEMANA_B)
        b2 = _parts(u2, SEMANA_B)
        b3 = _parts(u3, SEMANA_B)
        b4 = _parts(u4, SEMANA_B)
        b5 = _parts(u5, SEMANA_B)
        # u1, inativo, permanece na prata
        self.assertEqual(b1.liga_id, prata.id)
        self.assertFalse(b1.rebaixado)
        # u2, inativo no fim da prata, é rebaixado
        self.assertEqual(b2.liga_id, bronze.id)
        self.assertTrue(b2.rebaixado)
        self.assertEqual(b2.liga_anterior_id, prata.id)
        # u3, melhor da semana, é promovido
        self.assertEqual(b3.liga_id, prata.id)
        self.assertTrue(b3.promovido)
        self.assertEqual(b3.liga_anterior_id, bronze.id)
        # u4 permanece no bronze
        self.assertEqual(b4.liga_id, bronze.id)
        # u5, novo usuário, entra no bronze sem flags
        self.assertEqual(b5.liga_id, bronze.id)
        self.assertFalse(b5.promovido)
        self.assertFalse(b5.rebaixado)

    def test_nao_recalcula_semana_ja_processada(self):
        u1 = _usuario('u1')
        _log(u1, 100, datetime.combine(SEMANA_A, time(10)))
        calcular_ligas(semana=SEMANA_A)
        total = LigaParticipacao.objects.filter(semana=SEMANA_A).count()
        _usuario('u2')  # novo usuário não deve entrar sem forcar
        calcular_ligas(semana=SEMANA_A)
        self.assertEqual(LigaParticipacao.objects.filter(semana=SEMANA_A).count(), total)

    def test_recalcula_com_forca(self):
        u1 = _usuario('u1')
        _log(u1, 100, datetime.combine(SEMANA_A, time(10)))
        calcular_ligas(semana=SEMANA_A)
        u2 = _usuario('u2')
        _log(u2, 10, datetime.combine(SEMANA_A, time(11)))
        calcular_ligas(semana=SEMANA_A, forcar=True)
        self.assertEqual(LigaParticipacao.objects.filter(semana=SEMANA_A).count(), 2)

    def test_conta_admin_nao_compete_mas_staff_compete(self):
        u1 = _usuario('u1')
        admin = _usuario('admin')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        staff = _usuario('equipe')
        staff.is_staff = True
        staff.save()
        _log(u1, 100, datetime.combine(SEMANA_A, time(10)))
        _log(admin, 500, datetime.combine(SEMANA_A, time(11)))
        _log(staff, 200, datetime.combine(SEMANA_A, time(12)))

        calcular_ligas(semana=SEMANA_A)

        self.assertFalse(
            LigaParticipacao.objects.filter(usuario=admin, semana=SEMANA_A).exists()
        )
        p1 = _parts(u1, SEMANA_A)
        p_staff = _parts(staff, SEMANA_A)
        self.assertEqual(p1.xp_semana, 100)
        self.assertEqual(p_staff.xp_semana, 200)


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class RankingViewTest(TestCase):

    def setUp(self):
        self.user = _usuario('eu')
        self.other = _usuario('outro')
        _log(self.user, 60, datetime.combine(SEMANA_A, time(10)))
        _log(self.other, 30, datetime.combine(SEMANA_A, time(11)))
        calcular_ligas(semana=SEMANA_A)

    def test_tela_ranking_login_requerido(self):
        resp = self.client.get('/gamificacao/ranking/')
        self.assertEqual(resp.status_code, 302)

    def test_tela_ranking_mostra_liga_e_posicao(self):
        self.client.force_login(self.user)
        resp = self.client.get('/gamificacao/ranking/')
        self.assertEqual(resp.status_code, 200)
        participacao = resp.context['liga_part']
        self.assertIsNotNone(participacao)
        self.assertEqual(participacao.liga.nome, 'Prata')
        self.assertEqual(participacao.liga_anterior.nome, 'Prata')
        self.assertEqual(participacao.posicao, 1)
        self.assertEqual(resp.context['posicao_geral'], 1)
        self.assertEqual(len(resp.context['membros_liga']), 1)

    def test_painel_ranking_negado_para_nao_staff(self):
        self.client.force_login(self.user)
        resp = self.client.get('/painel/ranking/')
        self.assertEqual(resp.status_code, 302)

    def test_painel_recalcular_semana_inclui_tardios(self):
        self.other.is_staff = True
        self.other.save()
        novo = _usuario('novo')
        _log(novo, 20, datetime.combine(inicio_semana(), time(15)))
        self.client.force_login(self.other)
        resp = self.client.get('/painel/ranking/?recalcular=1')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['recalculado'])
        self.assertTrue(
            LigaParticipacao.objects.filter(
                usuario=novo, semana=inicio_semana()
            ).exists()
        )

    def test_painel_ranking_staff(self):
        self.other.is_staff = True
        self.other.is_superuser = True
        self.other.save()
        self.client.force_login(self.other)
        resp = self.client.get('/painel/ranking/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['secao'], 'ranking')
        self.assertEqual(len(resp.context['ligas_data']), 10)
        # staff competem no ranking; só a conta admin do seed fica fora
        self.assertEqual(len(resp.context['rows']), 2)