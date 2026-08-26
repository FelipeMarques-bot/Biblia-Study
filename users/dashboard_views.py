import json
from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Trilha, LicaoBiblica, ProgressoUsuario
from gamification.models import DesafioDiario, DesafioDiarioConcluido

@login_required
def dashboard_view(request):
    profile = request.user.profile
    hoje = date.today()

    # Streak
    streak = profile.streak_atual

    # XP da semana (dados reais)
    xp_semanal = []
    dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    for i in range(7):
        dia = hoje - timedelta(days=6 - i)
        xp_dia = ProgressoUsuario.objects.filter(
            usuario=request.user,
            concluida=True,
            data_conclusao__date=dia,
        ).values_list('xp_ganho_sessao', flat=True)
        xp_semanal.append({
            'day': dias_semana[i],
            'xp': sum(xp_dia),
        })
    xp_total = profile.xp_total
    xp_max = max(130, max((d['xp'] for d in xp_semanal), default=130))

    # Próxima lição
    licoes_concluidas = ProgressoUsuario.objects.filter(
        usuario=request.user, concluida=True
    ).values_list('licao_id', flat=True)

    proxima_licao = LicaoBiblica.objects.exclude(
        id__in=licoes_concluidas
    ).order_by('trilha__ordem', 'ordem').first()

    # Desafio do dia
    desafio_hoje = DesafioDiario.objects.filter(data=hoje).first()
    desafio_concluido = None
    if desafio_hoje:
        desafio_concluido = DesafioDiarioConcluido.objects.filter(
            usuario=request.user, desafio=desafio_hoje
        ).first()

    # Lições recentes
    licoes_recentes = ProgressoUsuario.objects.filter(
        usuario=request.user, concluida=True
    ).select_related('licao').order_by('-data_conclusao')[:5]

    return render(request, 'dashboard.html', {
        'user_full_name': request.user.get_full_name() or request.user.username,
        'streak': streak,
        'xp_semanal': json.dumps(xp_semanal),
        'xp_total': xp_total,
        'xp_max': xp_max,
        'nivel': profile.nivel,
        'nivel_progresso': profile.progresso_nivel(),
        'proxima_licao': proxima_licao,
        'desafio_hoje': desafio_hoje,
        'desafio_concluido': desafio_concluido,
        'licoes_recentes': licoes_recentes,
        'pontos_ajuda': profile.pontos_para_ajuda,
    })
