# -*- coding: utf-8 -*-
"""Ligas semanais estilo Duolingo: ranking, promocao e rebaixamento por etapa.

O calculo e feito sob demanda (nao depende de Celery/worker): ao abrir a pagina
de ranking, a semana vigente e processada e o resultado fica gravado em
`LigaParticipacao`, servindo de base para a evolucao (subir/regredir de etapa)
na semana seguinte.
"""
from datetime import date, timedelta
from math import ceil

from django.contrib.auth.models import User
from django.db.models import Sum

from users.models import UserProfile

from .models import Liga, LigaParticipacao, UserActivityLog

# Apenas a conta demo "admin" criada pelo seed não compete no ranking.
# Membro sênior (incl. superusuário) participa como usuário comum.
USUARIOS_ADMIN = ('admin',)

# Quantos usuários no topo/bottom de cada liga sobem/descem
TOP_PROMOCAO = 0.30
BOTTOM_REBAIXO = 0.15
# XP mínimo na semana para subir ou para não ser rebaixado
XP_PROMOCAO_MIN = 40
XP_PERMANENCIA_MIN = 15


def inicio_semana(dt=None):
    """Segunda-feira da semana que contém `dt`."""
    dt = dt or date.today()
    return dt - timedelta(days=dt.weekday())


def xp_por_usuario(semana):
    """Mapa {usuario_id: xp_ganho} na semana (início na segunda-feira).
    A conta administrativa (seed) não compete no ranking."""
    fim = semana + timedelta(days=7)
    logs = (
        UserActivityLog.objects
        .filter(data_hora__date__gte=semana, data_hora__date__lt=fim)
        .exclude(usuario__username__in=USUARIOS_ADMIN)
        .values('usuario_id')
        .annotate(total=Sum('xp_ganho'))
    )
    return {r['usuario_id']: r['total'] or 0 for r in logs}


def _perfis(participantes):
    return {
        p.usuario_id: p
        for p in UserProfile.objects.filter(usuario_id__in=participantes)
    }


def _xp_total(perfis, user_id):
    p = perfis.get(user_id)
    return getattr(p, 'xp_total', 0)


def calcular_ligas(semana=None, forcar=False):
    """Calcula e persiste as ligas da semana vigente. Retorna a semana usada."""
    semana = semana or inicio_semana()
    ligas = list(Liga.objects.order_by('ordem'))
    if not ligas:
        return semana
    ordem_maxima = ligas[-1].ordem
    liga_por_ordem = {l.ordem: l for l in ligas}

    if not forcar and LigaParticipacao.objects.filter(semana=semana).exists():
        # Mantém o cálculo já feito, apenas garante que a conta admin não participe
        LigaParticipacao.objects.filter(
            semana=semana, usuario__username__in=USUARIOS_ADMIN
        ).delete()
        return semana

    # Semana de referência = última participação registrada antes desta
    ref = LigaParticipacao.objects.filter(semana__lt=semana).order_by('-semana').first()
    if ref:
        ref_rows = list(
            LigaParticipacao.objects.filter(semana=ref.semana).select_related('liga')
        )
        refs = {r.usuario_id: r for r in ref_rows}
    else:
        refs = {}

    xp_semana = xp_por_usuario(semana)

    # Participantes: quem ganhou XP na semana ou estava na semana anterior.
    participantes = set(xp_semana.keys()) | set(refs.keys())
    if not participantes:
        participantes = set(
            User.objects.filter(is_active=True)
            .exclude(username__in=USUARIOS_ADMIN)
            .values_list('id', flat=True)
        )
    # A conta administrativa (seed) não compete no ranking
    participantes -= set(
        User.objects.filter(username__in=USUARIOS_ADMIN).values_list('id', flat=True)
    )

    perfis = _perfis(participantes)

    # Liga de origem (semana anterior) de cada participante
    bronze = liga_por_ordem.get(1, ligas[0])
    origem = {uid: (refs[uid].liga if uid in refs else bronze) for uid in participantes}

    # Agrupa por liga de origem e decide quem sobe/desce
    destino = {}
    por_origem = {}
    for uid, liga in origem.items():
        por_origem.setdefault(liga.id, []).append(uid)

    for membros in por_origem.values():
        liga = origem[membros[0]]
        membros.sort(
            key=lambda u: (xp_semana.get(u, 0), _xp_total(perfis, u)),
            reverse=True,
        )
        n = len(membros)
        if n >= 2 and liga.ordem < ordem_maxima:
            n_promover = max(1, ceil(n * TOP_PROMOCAO))
            for u in membros[:n_promover]:
                if xp_semana.get(u, 0) >= XP_PROMOCAO_MIN:
                    destino[u] = liga_por_ordem[liga.ordem + 1]
        if n >= 2 and liga.ordem > 1:
            n_rebaixar = max(1, ceil(n * BOTTOM_REBAIXO))
            for u in membros[-n_rebaixar:]:
                if xp_semana.get(u, 0) < XP_PERMANENCIA_MIN:
                    destino[u] = liga_por_ordem[liga.ordem - 1]

    # Quem não mudou permanece na liga de origem
    for uid, liga in origem.items():
        destino.setdefault(uid, liga)

    # Persistência
    LigaParticipacao.objects.filter(semana=semana).delete()
    registros = []
    por_liga = {}
    for uid, liga in destino.items():
        por_liga.setdefault(liga.id, []).append(uid)

    for membros in por_liga.values():
        liga = destino[membros[0]]
        membros.sort(
            key=lambda u: (xp_semana.get(u, 0), _xp_total(perfis, u)),
            reverse=True,
        )
        for posicao, uid in enumerate(membros, start=1):
            ref_row = refs.get(uid)
            liga_origem = origem.get(uid, bronze)
            registros.append(LigaParticipacao(
                usuario_id=uid,
                liga=liga,
                semana=semana,
                posicao=posicao,
                xp_semana=xp_semana.get(uid, 0),
                promovido=liga.ordem > liga_origem.ordem,
                rebaixado=liga.ordem < liga_origem.ordem,
                liga_anterior=liga_origem,
                posicao_anterior=ref_row.posicao if ref_row else 0,
            ))
    LigaParticipacao.objects.bulk_create(registros)
    return semana