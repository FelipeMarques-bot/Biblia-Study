import json
import random
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from .leagues import calcular_ligas, inicio_semana
from .models import (
    DesafioDiario, DesafioDiarioConcluido, Liga, LigaParticipacao,
    Recompensa, RecompensaUsuario,
    SerieOuroDesafio, SerieOuroExercicio, SerieOuroProgresso,
)
from .utils import log_activity

SEED_BASE_DATE = date(2024, 1, 1)


@login_required
def desafio_diario_view(request):
    hoje = timezone.now().date()
    day_of_year = hoje.timetuple().tm_yday
    idx = (day_of_year - 1) % 365
    target_date = SEED_BASE_DATE + timedelta(days=idx)

    desafio, created = DesafioDiario.objects.get_or_create(
        data=target_date,
        defaults={
            'titulo': 'Desafio do Dia',
            'descricao': 'Leia o versículo abaixo e reflita sobre como ele se aplica à sua vida.',
            'xp_recompensa': 30,
        }
    )
    concluido = DesafioDiarioConcluido.objects.filter(usuario=request.user, desafio=desafio).first()
    return render(request, 'desafio_diario.html', {
        'desafio': desafio,
        'concluido': concluido,
    })

@login_required
def concluir_desafio_diario(request, desafio_id):
    desafio = get_object_or_404(DesafioDiario, id=desafio_id)
    concluido, created = DesafioDiarioConcluido.objects.get_or_create(
        usuario=request.user,
        desafio=desafio,
        defaults={'xp_ganho': desafio.xp_recompensa}
    )
    if created:
        profile = request.user.profile
        profile.xp_total += desafio.xp_recompensa
        profile.pontos_para_ajuda += desafio.xp_recompensa // 2

        hoje = timezone.now().date()
        if profile.ultimo_dia_atividade is None:
            profile.streak_atual = 1
        elif profile.ultimo_dia_atividade == hoje:
            pass
        elif profile.ultimo_dia_atividade == hoje - timedelta(days=1):
            profile.streak_atual += 1
        else:
            profile.streak_atual = 1

        profile.ultimo_dia_atividade = hoje
        profile.save()
        log_activity(
            request.user, 'DESAFIO_DIARIO',
            descricao=f'Concluiu desafio: {desafio.titulo}',
            referencia=str(desafio.id),
            xp_ganho=desafio.xp_recompensa,
        )
    return JsonResponse({'success': True, 'xp': desafio.xp_recompensa})

@login_required
def recompensas_view(request):
    recompensas_disponiveis = Recompensa.objects.filter(ativo=True)
    user_recompensas = RecompensaUsuario.objects.filter(usuario=request.user)
    profile = request.user.profile
    licoes_feitas = profile.usuario.progresso.filter(concluida=True).count()

    pendentes = []
    for r in recompensas_disponiveis:
        if not user_recompensas.filter(recompensa=r).exists():
            if licoes_feitas >= r.criterio_licoes and profile.xp_total >= r.criterio_xp and profile.streak_atual >= r.criterio_streak:
                recomp, created = RecompensaUsuario.objects.get_or_create(
                    usuario=request.user, recompensa=r
                )
                pendentes.append(recomp)
        else:
            pendentes.append(user_recompensas.get(recompensa=r))

    recompensas_data = []
    for p in pendentes:
        recompensas_data.append({
            'id': p.id,
            'titulo': p.recompensa.titulo,
            'descricao': p.recompensa.descricao,
            'icone': p.recompensa.icone,
            'tipo': p.recompensa.get_tipo_display(),
            'xp': p.recompensa.xp_recompensa,
            'aberto': p.aberto,
        })

    return render(request, 'recompensas.html', {
        'recompensas': recompensas_data,
    })

@login_required
def abrir_bau(request, recompensa_id):
    recomp = get_object_or_404(RecompensaUsuario, id=recompensa_id, usuario=request.user)
    if not recomp.aberto:
        recomp.aberto = True
        recomp.save()
        profile = request.user.profile
        profile.xp_total += recomp.recompensa.xp_recompensa
        profile.save()
        log_activity(
            request.user, 'RECOMPENSA',
            descricao=f'Abril baú: {recomp.recompensa.titulo}',
            referencia=str(recomp.id),
            xp_ganho=recomp.recompensa.xp_recompensa,
        )
    return JsonResponse({
        'success': True,
        'titulo': recomp.recompensa.titulo,
        'descricao': recomp.recompensa.descricao,
        'icone': recomp.recompensa.icone,
        'xp': recomp.recompensa.xp_recompensa,
    })

@login_required
def serie_ouro_view(request):
    desafios = SerieOuroDesafio.objects.filter(ativo=True)
    progressos = SerieOuroProgresso.objects.filter(usuario=request.user)
    progresso_dict = {p.desafio_ouro_id: p for p in progressos}

    desafios_data = []
    for d in desafios:
        prog = progresso_dict.get(d.id)
        desafios_data.append({
            'id': d.id,
            'titulo': d.titulo,
            'descricao': d.descricao,
            'questoes': d.exercicios.count(),
            'xp': d.xp_recompensa,
            'concluido': prog.concluido if prog else False,
        })

    profile = request.user.profile
    return render(request, 'serie_ouro.html', {
        'desafios_data': desafios_data,
        'user_xp': profile.xp_total,
    })

@login_required
def serie_ouro_desafio_view(request, desafio_id):
    desafio = get_object_or_404(SerieOuroDesafio, id=desafio_id, ativo=True)
    exercicios = desafio.exercicios.all().order_by('id')

    progresso, created = SerieOuroProgresso.objects.get_or_create(
        usuario=request.user,
        desafio_ouro=desafio,
        defaults={'concluido': False}
    )

    if progresso.concluido:
        return render(request, 'serie_ouro_questoes.html', {
            'desafio': desafio,
            'exercicios_data': [],
            'ja_concluido': True,
        })

    exercicios_data = []
    for ex in exercicios:
        dados = ex.dados or {}
        pares = dados.get('pares', [])
        shuffled_right = [p['direita_correta'] for p in pares]
        random.shuffle(shuffled_right)
        itens = dados.get('itens', [])
        shuffled_order = list(range(len(itens)))
        random.shuffle(shuffled_order)

        exercicios_data.append({
            'id': ex.id,
            'tipo': ex.tipo,
            'pergunta': ex.enunciado,
            'dados': dados,
            'peso': ex.peso_dificuldade,
            'pares': pares,
            'shuffled_right': shuffled_right,
            'itens': itens,
            'shuffled_order': shuffled_order,
        })

    return render(request, 'serie_ouro_questoes.html', {
        'desafio': desafio,
        'exercicios_data': exercicios_data,
        'ja_concluido': False,
    })


@login_required
def serie_ouro_verificar_view(request, desafio_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    desafio = get_object_or_404(SerieOuroDesafio, id=desafio_id, ativo=True)
    data = json.loads(request.body)
    exercicio_id = data.get('exercicio_id')
    resposta = data.get('resposta')

    exercicio = get_object_or_404(SerieOuroExercicio, id=exercicio_id, desafio_ouro=desafio)

    correta = False
    dados = exercicio.dados or {}

    if exercicio.tipo in ('MULTIPLA_ESCOLHA', 'VF'):
        correta = resposta == dados.get('indice_correto')
    elif exercicio.tipo == 'ASSOCIACAO':
        pares = dados.get('pares', [])
        if isinstance(resposta, list) and len(resposta) == len(pares):
            correta = all(
                str(resposta[i]) == str(p['direita_correta'])
                for i, p in enumerate(pares)
            )
    elif exercicio.tipo == 'ORDENACAO':
        itens = dados.get('itens', [])
        if isinstance(resposta, list) and len(resposta) == len(itens):
            correta = resposta == list(range(len(itens)))

    xp = 0
    if correta:
        xp = exercicio.peso_dificuldade * 20
        profile = request.user.profile
        profile.xp_total += xp
        profile.pontos_para_ajuda += xp // 2
        profile.save()
        profile.atualizar_nivel_se_necessario()

    return JsonResponse({
        'correta': correta,
        'xp_ganho': xp,
        'dica': dados.get('dica', '') if not correta else None,
    })


@login_required
def serie_ouro_finalizar_view(request, desafio_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    desafio = get_object_or_404(SerieOuroDesafio, id=desafio_id, ativo=True)
    profile = request.user.profile

    progresso, _ = SerieOuroProgresso.objects.get_or_create(
        usuario=request.user,
        desafio_ouro=desafio,
    )

    if progresso.concluido:
        return JsonResponse({'success': True, 'xp_sessao': 0, 'ja_concluido': True})

    xp_bonus = desafio.xp_recompensa
    profile.xp_total += xp_bonus
    profile.pontos_para_ajuda += xp_bonus // 2

    hoje = timezone.now().date()
    if profile.ultimo_dia_atividade is None:
        profile.streak_atual = 1
    elif profile.ultimo_dia_atividade == hoje:
        pass
    elif profile.ultimo_dia_atividade == hoje - timedelta(days=1):
        profile.streak_atual += 1
    else:
        profile.streak_atual = 1

    profile.ultimo_dia_atividade = hoje
    profile.save()

    progresso.concluido = True
    progresso.data_conclusao = timezone.now()
    progresso.xp_ganho = xp_bonus
    progresso.save()

    nivel_mudou = profile.atualizar_nivel_se_necessario()

    log_activity(
        request.user, 'SERIE_OURO',
        descricao=f'Concluiu desafio ouro: {desafio.titulo}',
        referencia=str(desafio.id),
        xp_ganho=xp_bonus,
    )

    return JsonResponse({
        'success': True,
        'xp_total': profile.xp_total,
        'xp_sessao': xp_bonus,
        'streak': profile.streak_atual,
    })


@login_required
def abrir_bau_divino(request):
    import random
    profile = request.user.profile
    if profile.xp_total < 100:
        return JsonResponse({'error': 'XP insuficiente'}, status=400)
    xp_gasto = 50
    profile.xp_total -= xp_gasto
    profile.save()
    recompensas_bau = [
        {'tipo': 'Medalha de Ouro', 'texto': 'Fé Inabalável', 'xp': 500},
        {'tipo': 'Versículo', 'texto': 'Filipenses 4:13', 'xp': 200},
        {'tipo': 'Medalha', 'texto': 'Guerreiro da Palavra', 'xp': 300},
        {'tipo': 'Curiosidade', 'texto': 'A Bíblia tem 66 livros, 1189 capítulos e 31.102 versículos', 'xp': 150},
        {'tipo': 'Medalha de Prata', 'texto': 'Estudante Dedicado', 'xp': 350},
        {'tipo': 'Versículo', 'texto': 'Jeremias 29:11', 'xp': 200},
        {'tipo': 'XP Bônus', 'texto': 'XP Extra!', 'xp': 750},
        {'tipo': 'Medalha', 'texto': 'Corredor da Fé', 'xp': 400},
        {'tipo': 'Versículo', 'texto': 'Romanos 8:28', 'xp': 250},
        {'tipo': 'Medalha de Ouro', 'texto': 'Mestre da Escritura', 'xp': 600},
    ]
    premio = random.choice(recompensas_bau)
    profile.xp_total += premio['xp']
    profile.save()
    log_activity(
        request.user, 'RECOMPENSA',
        descricao=f'Baú Divino: {premio["texto"]}',
        referencia='bau_divino',
        xp_ganho=premio['xp'],
    )
    return JsonResponse({
        'success': True,
        'xp_gasto': xp_gasto,
        'xp_restante': profile.xp_total,
        'recompensa': premio,
    })


@login_required
def ranking_view(request):
    """Ranking estilo Duolingo: ligas semanais + posição global."""
    semana = calcular_ligas()
    usuario = request.user

    ranking_geral = list(
        User.objects.filter(is_active=True, is_staff=False)
        .select_related('profile')
        .order_by('-profile__xp_total', 'username')
    )
    posicao_geral = next(
        (i + 1 for i, u in enumerate(ranking_geral) if u.id == usuario.id), None
    )

    liga_part = (
        LigaParticipacao.objects
        .filter(usuario=usuario, semana=semana)
        .select_related('liga', 'liga_anterior')
        .first()
    )

    # Participantes da liga do usuário (semana atual)
    membros_liga = []
    if liga_part:
        participacoes = list(
            LigaParticipacao.objects
            .filter(semana=semana, liga=liga_part.liga)
            .select_related('liga', 'liga_anterior')
            .order_by('posicao')
        )
        usuarios = {
            u.id: u
            for u in User.objects.filter(
                id__in=[p.usuario_id for p in participacoes]
            ).select_related('profile')
        }
        membros_liga = [
            {'participacao': p, 'usuario': usuarios.get(p.usuario_id)}
            for p in participacoes
        ]

    ligas_ladder = list(Liga.objects.order_by('ordem'))

    evolucao = None
    if liga_part:
        if liga_part.promovido:
            evolucao = 'subiu'
        elif liga_part.rebaixado:
            evolucao = 'caiu'
        else:
            evolucao = 'manteve'

    return render(request, 'ranking.html', {
        'semana': semana,
        'semana_fim': inicio_semana() + timedelta(days=6),
        'usuario': usuario,
        'liga_part': liga_part,
        'membros_liga': membros_liga,
        'posicao_geral': posicao_geral,
        'total_usuarios': len(ranking_geral),
        'ranking_geral': ranking_geral[:10],
        'ligas_ladder': ligas_ladder,
        'evolucao': evolucao,
    })
