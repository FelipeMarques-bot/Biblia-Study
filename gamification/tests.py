# -*- coding: utf-8 -*-
from datetime import date, datetime, time

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils import timezone

from .leagues import inicio_semana, calcular_ligas
from .models import (
    Liga,
    LigaParticipacao,
    SerieOuroDesafio,
    SerieOuroExercicio,
    SerieOuroProgresso,
    UserActivityLog,
)

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


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class SerieOuroTest(TestCase):

    def setUp(self):
        self.user = _usuario('ouro')
        self.desafio = SerieOuroDesafio.objects.create(
            titulo='Ouro: Teste',
            descricao='teste',
            ativo=True,
            xp_recompensa=400,
        )
        self.client.force_login(self.user)

    def _streak(self, n):
        self.user.profile.streak_atual = n
        self.user.profile.ultimo_dia_atividade = timezone.now().date()
        self.user.profile.save()

    def _streak_parado(self, n, dias_sem_atividade):
        """Streak congelado no banco, mas há ``dias_sem_atividade`` sem estudar."""
        self.user.profile.streak_atual = n
        self.user.profile.ultimo_dia_atividade = timezone.now().date() - timezone.timedelta(days=dias_sem_atividade)
        self.user.profile.save()

    def test_lista_bloqueada_abaixo_de_3_dias(self):
        self._streak(2)
        resp = self.client.get('/gamificacao/serie-ouro/')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['liberado'])
        self.assertEqual(resp.context['streak_atual'], 2)

    def test_desafio_redireciona_abaixo_de_3_dias(self):
        self._streak(2)
        resp = self.client.get(f'/gamificacao/serie-ouro/{self.desafio.id}/')
        self.assertEqual(resp.status_code, 302)

    def test_verificar_negado_abaixo_de_3_dias(self):
        self._streak(2)
        resp = self.client.post(
            f'/gamificacao/serie-ouro/{self.desafio.id}/verificar/',
            data='{"exercicio_id": 1, "resposta": 0}',
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 403)

    def test_finalizar_negado_abaixo_de_3_dias(self):
        self._streak(2)
        resp = self.client.post(
            f'/gamificacao/serie-ouro/{self.desafio.id}/finalizar/',
            data='{}',
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(
            SerieOuroProgresso.objects.filter(
                usuario=self.user, desafio_ouro=self.desafio
            ).exists()
        )

    def test_bau_divino_negado_abaixo_de_3_dias(self):
        self._streak(2)
        self.user.profile.xp_total = 500
        self.user.profile.save()
        resp = self.client.post(
            '/gamificacao/serie-ouro/abrir-bau/',
            data='{}',
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 403)

    def test_bau_divino_liberado_com_3_dias(self):
        self._streak(3)
        self.user.profile.xp_total = 500
        self.user.profile.save()
        resp = self.client.post(
            '/gamificacao/serie-ouro/abrir-bau/',
            data='{}',
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recompensa', resp.json())

    def test_liberada_com_3_dias(self):
        self._streak(3)
        resp = self.client.get('/gamificacao/serie-ouro/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['liberado'])
        resp2 = self.client.get(f'/gamificacao/serie-ouro/{self.desafio.id}/')
        self.assertEqual(resp2.status_code, 200)

    def test_streak_fantasma_apos_2_dias_parado_bloqueia_bau(self):
        # Usuário alcançou 3 dias, mas ficou 2 dias sem estudar:
        # o valor salvo continua 3, porém o baú NÃO pode mais abrir.
        self._streak_parado(3, dias_sem_atividade=2)
        self.user.profile.xp_total = 500
        self.user.profile.save()
        resp = self.client.post(
            '/gamificacao/serie-ouro/abrir-bau/',
            data='{}',
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 403)

    def test_streak_fantasma_apos_2_dias_parado_bloqueia_serie(self):
        self._streak_parado(3, dias_sem_atividade=2)
        resp = self.client.get('/gamificacao/serie-ouro/')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['liberado'])
        resp2 = self.client.get(f'/gamificacao/serie-ouro/{self.desafio.id}/')
        self.assertEqual(resp2.status_code, 302)

    def test_ultimo_dia_ainda_pode_continuar_constancia(self):
        # Ontem houve atividade: hoje ainda pode completar o dia da série.
        self._streak_parado(3, dias_sem_atividade=1)
        self.user.profile.xp_total = 500
        self.user.profile.save()
        resp = self.client.post(
            '/gamificacao/serie-ouro/abrir-bau/',
            data='{}',
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)

    def test_pagina_mostra_semana_e_ultima_atividade(self):
        self._streak(3)
        _log(self.user, 30, datetime.combine(timezone.now().date(), time(10)))
        resp = self.client.get('/gamificacao/serie-ouro/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['semana_dias']), 7)
        self.assertEqual(resp.context['ultima_atividade'], timezone.now().date())
        hoje = [d for d in resp.context['semana_dias'] if d['hoje']][0]
        self.assertTrue(hoje['ativo'])