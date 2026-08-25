import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    Trilha, LicaoBiblica, Exercicio, ProgressoUsuario,
    ExercisePool, PerformanceTracker, GeneratedLesson,
)
from gamification.utils import log_activity


@login_required
def lista_trilhas(request):
    trilhas = Trilha.objects.filter(ativo=True).order_by('ordem')

    profile = request.user.profile
    trilhas_data = []
    for t in trilhas:
        licoes_count = t.licoes.count()
        concluidas = ProgressoUsuario.objects.filter(
            usuario=request.user, licao__trilha=t, concluida=True
        ).count()
        progresso = int((concluidas / licoes_count) * 100) if licoes_count > 0 else 0

        trilhas_data.append({
            'id': t.id,
            'nome': t.nome,
            'descricao': t.descricao,
            'icone': t.icone,
            'faixa_etaria': t.get_faixa_etaria_display(),
            'nivel': t.get_nivel_display(),
            'licoes_count': licoes_count,
            'concluidas': concluidas,
            'progresso': progresso,
        })

    return render(request, 'trilhas.html', {
        'trilhas': trilhas,
        'trilhas_data': json.dumps(trilhas_data),
    })


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
        'trilhas': Trilha.objects.filter(ativo=True),
        'licoes_data': json.dumps(licoes_data),
        'show_map': True,
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

    xp = 0
    if correta:
        xp = exercicio.peso_dificuldade * 20
        profile = request.user.profile
        profile.xp_total += xp
        profile.pontos_para_ajuda += xp // 2
        profile.save()
        progresso.xp_ganho_sessao += xp
        profile.atualizar_nivel_se_necessario()

    respostas = progresso.respostas or {}
    respostas[str(exercicio_id)] = {'resposta': resposta, 'correta': correta}
    progresso.respostas = respostas
    progresso.save()

    topico = _obter_topico_licao(licao)
    dificuldade = min(exercicio.peso_dificuldade, 4)
    tracker, _ = PerformanceTracker.objects.get_or_create(
        usuario=request.user,
        topico=topico,
        dificuldade=dificuldade,
    )
    tracker.total_questoes += 1
    if correta:
        tracker.acertos += 1
        tracker.combo_atual += 1
        tracker.combo_maximo = max(tracker.combo_maximo, tracker.combo_atual)
    else:
        tracker.erros += 1
        tracker.combo_atual = 0
    tracker.ultima_questao_data = timezone.now()
    tracker.save()

    combo_multiplier = 1 + (tracker.combo_atual * 0.1) if correta else 0
    xp_com_bonus = round(xp * combo_multiplier) if combo_multiplier > 0 else 0

    return JsonResponse({
        'correta': correta,
        'xp_ganho': xp_com_bonus if correta else 0,
        'xp_base': xp,
        'combo': tracker.combo_atual if correta else 0,
        'combo_multiplier': round(combo_multiplier, 1) if correta else 1.0,
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

    nivel_mudou = profile.atualizar_nivel_se_necessario()

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
        'nivel': profile.nivel_atual,
        'nivel_mudou': nivel_mudou,
    })


@login_required
def gerar_exercicios_ia(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    data = json.loads(request.body)
    topico = data.get('topico', 'novo_testamento')
    quantidade = min(data.get('quantidade', 5), 10)

    profile = request.user.profile
    nivel_map = {'iniciante': 1, 'intermediario': 2, 'avancado': 3, 'mestre': 4}
    dificuldade = nivel_map.get(profile.nivel_atual, 1)

    pool = ExercisePool.objects.filter(
        topico=topico, dificuldade__lte=dificuldade, ativo=True,
    ).order_by('?')[:quantidade]

    exercicios_data = []
    for ex in pool:
        exercicios_data.append({
            'id': f'pool_{ex.id}',
            'tipo': ex.tipo,
            'pergunta': ex.enunciado,
            'dados': ex.dados,
            'peso': ex.peso_dificuldade,
            'fonte': 'pool',
        })
        ex.vezes_usado += 1
        ex.save(update_fields=['vezes_usado'])

    if len(exercicios_data) < quantidade:
        ia_exercicios = _gerar_exercicios_ia(topico, dificuldade, quantidade - len(exercicios_data))
        exercicios_data.extend(ia_exercicios)

    return JsonResponse({
        'exercicios': exercicios_data,
        'dificuldade': dificuldade,
        'topico': topico,
    })


@login_required
def gerar_licao_ia(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    data = json.loads(request.body)
    topico = data.get('topico', 'novo_testamento')
    profile = request.user.profile

    nivel_map = {'iniciante': 1, 'intermediario': 2, 'avancado': 3, 'mestre': 4}
    dificuldade = nivel_map.get(profile.nivel_atual, 1)

    try:
        from ia_engine.engine import _call_llm
        prompt = f"""
Crie uma lição bíblica curta sobre "{topico}" para nível {dificuldade}/4.
Retorne APENAS um JSON válido com esta estrutura:
{{
    "titulo": "Título da Lição",
    "referencia": "Referência bíblica",
    "conteudo": "Conteúdo explicativo (3-4 parágrafos curtos)",
    "exercicios": [
        {{
            "tipo": "MULTIPLA_ESCOLHA",
            "enunciado": "Pergunta",
            "dados": {{
                "alternativas": ["A", "B", "C", "D"],
                "indice_correto": 0,
                "dica": "Dica curta"
            }},
            "dificuldade": 1
        }}
    ]
}}
Gere 3 exercícios variados. Tom pastoral e reformado.
"""
        resposta = _call_llm(prompt, temperature=0.5)

        import re
        json_match = re.search(r'\{[\s\S]*\}', resposta)
        if json_match:
            licao_data = json.loads(json_match.group())
        else:
            raise ValueError('JSON não encontrado')

        lesson = GeneratedLesson.objects.create(
            usuario=request.user,
            titulo=licao_data.get('titulo', f'Lição sobre {topico}'),
            topico=topico,
            dificuldade=dificuldade,
            referencia_biblica=licao_data.get('referencia', ''),
            conteudo_gerado=licao_data.get('conteudo', ''),
            exercicios_gerados=licao_data.get('exercicios', []),
            xp_recompensa=50 * dificuldade,
        )

        return JsonResponse({
            'success': True,
            'licao': {
                'id': lesson.id,
                'titulo': lesson.titulo,
                'referencia': lesson.referencia_biblica,
                'conteudo': lesson.conteudo_gerado,
                'exercicios': lesson.exercicios_gerados,
                'xp_recompensa': lesson.xp_recompensa,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def performance_view(request):
    trackers = PerformanceTracker.objects.filter(usuario=request.user)
    performance = []
    for t in trackers:
        performance.append({
            'topico': t.topico,
            'topico_display': t.get_topico_display(),
            'dificuldade': t.dificuldade,
            'dificuldade_display': t.get_dificuldade_display(),
            'total': t.total_questoes,
            'acertos': t.acertos,
            'taxa_acerto': round(t.taxa_acerto * 100),
            'combo_maximo': t.combo_maximo,
        })
    return JsonResponse({'performance': performance})


def _obter_topico_licao(licao):
    titulo_lower = licao.titulo.lower()
    trilha_nome = licao.trilha.nome.lower() if licao.trilha else ''

    if 'gênesis' in titulo_lower or 'genesis' in titulo_lower or 'criação' in titulo_lower:
        return 'genesis'
    elif 'êxodo' in titulo_lower or 'exodo' in titulo_lower:
        return 'exodo'
    elif 'salmo' in titulo_lower or 'salmos' in titulo_lower:
        return 'psalmos'
    elif 'provérbio' in titulo_lower or 'proverbio' in titulo_lower:
        return 'proverbios'
    elif 'isaías' in titulo_lower or 'isaias' in titulo_lower:
        return 'isaias'
    elif 'mateus' in titulo_lower:
        return 'mateus'
    elif 'joão' in titulo_lower or 'joao' in titulo_lower:
        return 'joao'
    elif 'roman' in titulo_lower:
        return 'romanos'
    elif 'efésio' in titulo_lower or 'efesio' in titulo_lower:
        return 'efesios'
    elif 'hebreu' in titulo_lower:
        return 'hebreus'
    elif 'apocalipse' in titulo_lower or 'revelação' in titulo_lower:
        return 'revelacao'
    elif 'ato' in titulo_lower:
        return 'atos'
    elif 'evangelho' in titulo_lower or 'jesus' in titulo_lower:
        return 'gospels'
    elif 'epístola' in titulo_lower or 'epistola' in titulo_lower or 'paulo' in titulo_lower:
        return 'epistolas'
    elif 'antigo' in trilha_nome:
        return 'antigo_testamento'
    elif 'novo' in trilha_nome:
        return 'novo_testamento'
    return 'novo_testamento'


def _gerar_exercicios_ia(topico, dificuldade, quantidade):
    try:
        from ia_engine.engine import _call_llm
        prompt = f"""
Gere {quantidade} exercícios bíblicos sobre "{topico}" nível {dificuldade}/4.
Retorne APENAS um JSON válido com esta estrutura:
{{
    "exercicios": [
        {{
            "tipo": "MULTIPLA_ESCOLHA",
            "enunciado": "Pergunta",
            "dados": {{"alternativas": ["A","B","C","D"], "indice_correto": 0, "dica": "Dica"}},
            "dificuldade": 1
        }}
    ]
}}
Varie os tipos. Tom pastoral.
"""
        resposta = _call_llm(prompt, temperature=0.5)

        import re
        json_match = re.search(r'\{[\s\S]*\}', resposta)
        if json_match:
            data = json.loads(json_match.group())
            resultado = []
            for ex in data.get('exercicios', [])[:quantidade]:
                resultado.append({
                    'id': f'ia_{hash(ex.get("enunciado", "")) % 100000}',
                    'tipo': ex.get('tipo', 'MULTIPLA_ESCOLHA'),
                    'pergunta': ex.get('enunciado', ''),
                    'dados': ex.get('dados', {}),
                    'peso': ex.get('dificuldade', dificuldade),
                    'fonte': 'ia',
                })
            return resultado
    except Exception:
        pass
    return []
