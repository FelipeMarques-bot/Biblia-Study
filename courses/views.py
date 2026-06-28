import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Trilha, LicaoBiblica, Exercicio, ProgressoUsuario
from django.utils import timezone
from gamification.utils import log_activity

@login_required
def lista_trilhas(request):
    trilhas = Trilha.objects.filter(ativo=True)
    return render(request, 'trilhas.html', {'trilhas': trilhas})

@login_required
def mapa_trilha(request, trilha_id):
    trilha = get_object_or_404(Trilha, id=trilha_id)
    licoes = trilha.licoes.all().order_by('ordem')
    progressos = ProgressoUsuario.objects.filter(usuario=request.user, licao__in=licoes)
    progresso_dict = {p.licao_id: p for p in progressos}

    licoes_data = []
    for l in licoes:
        prog = progresso_dict.get(l.id)
        if prog and prog.concluida:
            status = 'completed'
        elif prog and not prog.concluida:
            status = 'active'
        else:
            status = 'locked'
        licoes_data.append({
            'id': l.id,
            'titulo': l.titulo,
            'icone': l.trilha.icone,
            'status': status,
            'ordem': l.ordem,
        })

    return render(request, 'trilhas.html', {
        'trilha': trilha,
        'licoes_data': json.dumps(licoes_data),
    })

@login_required
def licao_view(request, licao_id):
    licao = get_object_or_404(LicaoBiblica, id=licao_id)
    exercicios = licao.exercicios.all().order_by('ordem')

    progresso, created = ProgressoUsuario.objects.get_or_create(
        usuario=request.user,
        licao=licao,
        defaults={'data_inicio': timezone.now()}
    )

    exercicios_data = []
    for ex in exercicios:
        exercicios_data.append({
            'id': ex.id,
            'tipo': ex.tipo,
            'pergunta': ex.enunciado,
            'dados': ex.dados,
            'peso': ex.peso_dificuldade,
        })

    return render(request, 'licao.html', {
        'licao': licao,
        'exercicios_data': json.dumps(exercicios_data),
    })

@login_required
def verificar_resposta(request, licao_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    licao = get_object_or_404(LicaoBiblica, id=licao_id)
    data = json.loads(request.body)
    exercicio_id = data.get('exercicio_id')
    resposta = data.get('resposta')

    exercicio = get_object_or_404(Exercicio, id=exercicio_id, licao=licao)
    progresso, _ = ProgressoUsuario.objects.get_or_create(
        usuario=request.user, licao=licao
    )

    correta = False
    if exercicio.tipo in ('MULTIPLA_ESCOLHA', 'VF'):
        correta = resposta == exercicio.dados.get('indice_correto')
    elif exercicio.tipo == 'ASSOCIACAO':
        pares = exercicio.dados.get('pares', [])
        if isinstance(resposta, list) and len(resposta) == len(pares):
            correta = all(
                str(resposta[i]) == str(p['direita_correta'])
                for i, p in enumerate(pares)
            )
    elif exercicio.tipo == 'ORDENACAO':
        itens = exercicio.dados.get('itens', [])
        if isinstance(resposta, list) and len(resposta) == len(itens):
            correta = resposta == list(range(len(itens)))

    if correta:
        xp = exercicio.peso_dificuldade * 20
        profile = request.user.profile
        profile.xp_total += xp
        profile.pontos_para_ajuda += xp // 2
        profile.save()
        progresso.xp_ganho_sessao += xp

    respostas = progresso.respostas or {}
    respostas[str(exercicio_id)] = {'resposta': resposta, 'correta': correta}
    progresso.respostas = respostas
    progresso.save()

    return JsonResponse({
        'correta': correta,
        'xp_ganho': xp if correta else 0,
        'dica': exercicio.dados.get('dica', '') if not correta else None,
    })

@login_required
def finalizar_licao(request, licao_id):
    licao = get_object_or_404(LicaoBiblica, id=licao_id)
    progresso = get_object_or_404(ProgressoUsuario, usuario=request.user, licao=licao)

    profile = request.user.profile
    xp_bonus = licao.xp_recompensa
    profile.xp_total += xp_bonus
    profile.pontos_para_ajuda += xp_bonus // 2

    profile.streak_atual += 1
    profile.ultimo_dia_atividade = timezone.now().date()
    profile.save()

    progresso.concluida = True
    progresso.data_conclusao = timezone.now()
    progresso.xp_ganho_sessao += xp_bonus
    progresso.save()

    log_activity(
        request.user, 'LICAO_CONCLUIDA',
        descricao=f'Concluiu a lição: {licao.titulo}',
        referencia=str(licao.id),
        xp_ganho=progresso.xp_ganho_sessao,
    )

    return JsonResponse({
        'success': True,
        'xp_total': profile.xp_total,
        'xp_sessao': progresso.xp_ganho_sessao,
        'streak': profile.streak_atual,
        'baú_disponivel': profile.xp_total > 100 and profile.xp_total % 100 < 50,
    })
