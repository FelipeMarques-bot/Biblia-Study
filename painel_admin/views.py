import csv
from datetime import date, datetime, timedelta
from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Sum, Q
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import (
    Exercicio,
    GeneratedLesson,
    LicaoBiblica,
    ProgressoUsuario,
    Trilha,
)
from gamification.leagues import USUARIOS_ADMIN, calcular_ligas, xp_por_usuario
from gamification.models import (
    DesafioDiario,
    DesafioDiarioConcluido,
    Liga,
    LigaParticipacao,
    Recompensa,
    RecompensaUsuario,
    SerieOuroProgresso,
    UserActivityLog,
)
from users.models import FAIXA_ETARIA_CHOICES, NIVEL_CHOICES, UserProfile

TIPO_ATIVIDADE_LABELS = dict(UserActivityLog.TIPO_CHOICES)
TIPO_ATIVIDADE_ICONES = {
    'LICAO_CONCLUIDA': '📖',
    'DESAFIO_DIARIO': '⚡',
    'SERIE_OURO': '🏆',
    'CHAT_DEVOCIONAL': '💬',
    'DICA_IA': '💡',
    'EXPLICACAO_IA': '🤖',
    'RECOMPENSA': '🏅',
    'LOGIN': '🔑',
}

NIVEL_STYLE = {
    'iniciante': 'bg-neon-green/15 text-neon-green border-neon-green/20',
    'intermediario': 'bg-neon-blue/15 text-neon-blue border-neon-blue/20',
    'avancado': 'bg-neon-purple/15 text-neon-purple border-neon-purple/20',
    'mestre': 'bg-neon-gold/15 text-neon-gold border-neon-gold/20',
    'super_cristao': 'bg-neon-pink/10 text-neon-pink border-neon-pink/30',
}

FAIXA_ICONE = {
    'crianca': '🧒',
    'adolescente': '🧑‍🎓',
    'adulto': '🧑',
}


def painel_requerido(view_func):
    """Exige usuário autenticado e staff para acessar o painel."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('painel:login')
        if not request.user.is_staff:
            messages.error(request, 'Acesso restrito ao painel administrativo.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped


def painel_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('painel:dashboard')
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            if user.is_staff:
                return redirect('painel:dashboard')
            messages.warning(request, 'Essa conta não possui acesso ao painel administrativo.')
            return redirect('dashboard')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'painel_admin/login.html')


def _paginas(paginator, pagina_atual, janela=2):
    """Gera lista de páginas para paginação com reticências."""
    numeros = sorted(set(
        list(paginator.page_range[:janela])
        + list(paginator.page_range[-janela:])
        + list(range(max(1, pagina_atual - janela), min(paginator.num_pages, pagina_atual + janela) + 1))
    ))
    resultado = []
    anterior = None
    for n in numeros:
        if anterior is not None and n - anterior > 1:
            resultado.append(None)
        resultado.append(n)
        anterior = n
    return resultado


@painel_requerido
def dashboard(request, *args, **kwargs):
    hoje = date.today()
    ultimos_30 = hoje - timedelta(days=29)
    ultimos_8 = hoje - timedelta(weeks=8)

    # KPI
    total_usuarios = User.objects.count()
    novos_hoje = User.objects.filter(date_joined__date=hoje).count()
    ativos_hoje = User.objects.filter(last_login__date=hoje).count()
    staff_count = User.objects.filter(is_staff=True).count()
    xp_total = UserProfile.objects.aggregate(t=Sum('xp_total'))['t'] or 0
    licoes_concluidas = ProgressoUsuario.objects.filter(concluida=True).count()
    desafios_concluidos = DesafioDiarioConcluido.objects.count()
    recompensas_desbloqueadas = RecompensaUsuario.objects.count()
    media_streak = int(UserProfile.objects.aggregate(m=Avg('streak_atual'))['m'] or 0)
    maior_streak = UserProfile.objects.aggregate(m=Max('streak_atual'))['m'] or 0
    sessoes_chat = UserActivityLog.objects.filter(tipo_atividade='CHAT_DEVOCIONAL').count()

    # Registros por dia (últimos 30 dias)
    registros_qs = (
        User.objects.filter(date_joined__date__gte=ultimos_30)
        .annotate(d=TruncDate('date_joined'))
        .values('d')
        .annotate(n=Count('id'))
        .order_by('d')
    )
    registros_por_dia = {r['d']: r['n'] for r in registros_qs}
    dias_labels = [(hoje - timedelta(days=i)).strftime('%d/%m') for i in range(29, -1, -1)]
    registros_serie = [registros_por_dia.get(hoje - timedelta(days=29 - i), 0) for i in range(30)]

    # Atividades por tipo (últimos 30 dias)
    atividades_tipo_qs = (
        UserActivityLog.objects.filter(data_hora__date__gte=ultimos_30)
        .values('tipo_atividade')
        .annotate(n=Count('id'))
        .order_by('-n')
    )
    atividades_por_tipo = {
        TIPO_ATIVIDADE_LABELS.get(a['tipo_atividade'], a['tipo_atividade']): a['n']
        for a in atividades_tipo_qs
    }

    # Top 10 usuários por XP (sem a conta administrativa do seed)
    top_usuarios = (
        UserProfile.objects.select_related('usuario')
        .exclude(usuario__username__in=USUARIOS_ADMIN)
        .order_by('-xp_total')[:10]
    )
    top_nomes = [p.usuario.username for p in top_usuarios]
    top_xp = [p.xp_total for p in top_usuarios]

    # XP por semana (últimas 8 semanas)
    logs = UserActivityLog.objects.filter(
        data_hora__date__gte=ultimos_8
    ).values('data_hora', 'xp_ganho')

    semana_xp = {i: 0 for i in range(8)}
    for log in logs:
        d = log['data_hora'].date()
        index = (d - ultimos_8).days // 7 if d >= ultimos_8 else 0
        index = min(7, max(0, index))
        semana_xp[index] += log['xp_ganho'] or 0

    semana_labels = [
        (ultimos_8 + timedelta(days=7 * i)).strftime('%d/%m')
        for i in range(8)
    ]
    semana_serie = [semana_xp[i] for i in range(8)]

    # Últimas atividades
    atividades_recentes = (
        UserActivityLog.objects.select_related('usuario').order_by('-data_hora')[:8]
    )

    context = {
        'secao': 'dashboard',
        'kpi': {
            'total_usuarios': total_usuarios,
            'novos_hoje': novos_hoje,
            'ativos_hoje': ativos_hoje,
            'staff_count': staff_count,
            'xp_total': xp_total,
            'licoes_concluidas': licoes_concluidas,
            'desafios_concluidos': desafios_concluidos,
            'recompensas_desbloqueadas': recompensas_desbloqueadas,
            'media_streak': media_streak,
            'maior_streak': maior_streak,
            'sessoes_chat': sessoes_chat,
        },
        'dias_labels': dias_labels,
        'registros_serie': registros_serie,
        'atividades_por_tipo': atividades_por_tipo,
        'top_nomes': top_nomes,
        'top_xp': top_xp,
        'semana_labels': semana_labels,
        'semana_serie': semana_serie,
        'atividades_recentes': atividades_recentes,
        'hoje': hoje,
    }
    return render(request, 'painel_admin/dashboard.html', context)


@painel_requerido
def usuarios(request, *args, **kwargs):
    qs = User.objects.select_related('profile')

    q = request.GET.get('q', '').strip()
    faixa = request.GET.get('faixa', '')
    nivel = request.GET.get('nivel', '')
    staff = request.GET.get('staff', '')
    ativo = request.GET.get('ativo', '')
    ordenar = request.GET.get('ordenar', 'data')
    direcao = request.GET.get('direcao', 'desc')

    if q:
        qs = qs.filter(
            Q(username__icontains=q)
            | Q(email__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
        )
    if faixa:
        qs = qs.filter(profile__faixa_etaria=faixa)
    if nivel:
        qs = qs.filter(profile__nivel_atual=nivel)
    if staff in ('true', 'false'):
        qs = qs.filter(is_staff=(staff == 'true'))
    if ativo in ('true', 'false'):
        qs = qs.filter(is_active=(ativo == 'true'))

    campos_ordenacao = {
        'data': 'date_joined',
        'nome': 'username',
        'xp': 'profile__xp_total',
        'streak': 'profile__streak_atual',
        'nivel': 'profile__nivel_atual',
        'ultimo_acesso': 'last_login',
    }
    prefixo = '-' if direcao == 'desc' else ''
    qs = qs.order_by(f'{prefixo}{campos_ordenacao.get(ordenar, "date_joined")}')

    paginator = Paginator(qs, 30)
    num_pagina = request.GET.get('pagina', 1)
    try:
        pagina_obj = paginator.page(num_pagina)
    except Exception:
        pagina_obj = paginator.page(1)

    faixas = [{'valor': v, 'label': l} for v, l in FAIXA_ETARIA_CHOICES]
    niveis = [{'valor': v, 'label': l} for v, l in NIVEL_CHOICES]

    context = {
        'secao': 'usuarios',
        'usuarios': pagina_obj,
        'paginas': _paginas(paginator, pagina_obj.number),
        'total': paginator.count,
        'filtros': {
            'q': q, 'faixa': faixa, 'nivel': nivel, 'staff': staff,
            'ativo': ativo, 'ordenar': ordenar, 'direcao': direcao,
        },
        'faixas': faixas,
        'niveis': niveis,
    }
    return render(request, 'painel_admin/usuarios.html', context)


@painel_requerido
def exportar_usuarios_csv(request, *args, **kwargs):
    qs = User.objects.select_related('profile').order_by('-date_joined')
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'
    response.write('\ufeff')
    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'ID', 'Nome', 'Email', 'Usuário', 'Ativo', 'Staff',
        'Faixa Etária', 'Nível', 'XP Total', 'Streak', 'Último Acesso', 'Criado em',
    ])
    for u in qs:
        writer.writerow([
            u.id, (u.get_full_name() or u.username), u.email, u.username,
            'Sim' if u.is_active else 'Não', 'Sim' if u.is_staff else 'Não',
            u.profile.get_faixa_etaria_display(), u.profile.get_nivel_atual_display(),
            u.profile.xp_total, u.profile.streak_atual,
            u.last_login.strftime('%d/%m/%Y %H:%M') if u.last_login else '',
            u.date_joined.strftime('%d/%m/%Y %H:%M'),
        ])
    return response


@painel_requerido
def usuario_detalhe(request, user_id):
    usuario = get_object_or_404(User.objects.select_related('profile'), id=user_id)
    perfil = usuario.profile

    licoes_ok = ProgressoUsuario.objects.filter(usuario=usuario, concluida=True)
    desafios_ok = DesafioDiarioConcluido.objects.filter(usuario=usuario)
    serie_ouro_ok = SerieOuroProgresso.objects.filter(usuario=usuario, concluido=True)
    recompensas = RecompensaUsuario.objects.filter(usuario=usuario).select_related('recompensa')
    atividades = (
        UserActivityLog.objects.filter(usuario=usuario)
        .order_by('-data_hora')[:30]
    )
    licoes_geradas = GeneratedLesson.objects.filter(usuario=usuario).count()
    sessoes_devocionais = usuario.sessoes_devocionais.count()

    progresso_por_licao = (
        ProgressoUsuario.objects.filter(usuario=usuario, concluida=True)
        .select_related('licao__trilha')
        .order_by('licao__trilha__ordem', 'licao__ordem')
    )

    # XP por dia (últimos 30 dias)
    ultimos_30 = date.today() - timedelta(days=29)
    logs = (
        UserActivityLog.objects.filter(
            usuario=usuario, data_hora__date__gte=ultimos_30
        )
        .extra(select={'dia': "date(data_hora)"})
        .values('dia')
        .annotate(xp=Sum('xp_ganho'))
        .order_by('dia')
    )
    xp_por_dia = {r['dia']: r['xp'] for r in logs}
    xp_labels = [(date.today() - timedelta(days=i)).strftime('%d/%m') for i in range(29, -1, -1)]
    xp_serie = [xp_por_dia.get(date.today() - timedelta(days=29 - i), 0) for i in range(30)]

    # Agrupa progresso por trilha
    trilhas_progresso = []
    por_trilha = {}
    for item in progresso_por_licao:
        chave = item.licao.trilha_id
        d = por_trilha.setdefault(chave, {
            'nome': item.licao.trilha.nome,
            'icone': item.licao.trilha.icone,
            'feitas': 0,
            'total': LicaoBiblica.objects.filter(trilha_id=chave).count(),
            'xp': 0,
        })
        d['feitas'] += 1
        d['xp'] += item.xp_ganho_sessao
    trilhas_progresso = list(por_trilha.values())

    context = {
        'secao': 'usuarios',
        'usuario': usuario,
        'perfil': perfil,
        'kpi': {
            'licoes': licoes_ok.count(),
            'desafios': desafios_ok.count(),
            'serie_ouro': serie_ouro_ok.count(),
            'recompensas': recompensas.count(),
            'licoes_geradas': licoes_geradas,
            'sessoes_devocionais': sessoes_devocionais,
        },
        'recompensas': recompensas,
        'atividades': atividades,
        'trilhas_progresso': trilhas_progresso,
        'xp_labels': xp_labels,
        'xp_serie': xp_serie,
        'faixa_icone': FAIXA_ICONE.get(perfil.faixa_etaria, '🧑'),
        'nivel_style': NIVEL_STYLE.get(perfil.nivel_atual, NIVEL_STYLE['iniciante']),
        'tipo_icon': TIPO_ATIVIDADE_ICONES,
    }
    return render(request, 'painel_admin/usuario_detalhe.html', context)


@painel_requerido
def atividades(request, *args, **kwargs):
    qs = UserActivityLog.objects.select_related('usuario')

    tipo = request.GET.get('tipo', '')
    q = request.GET.get('q', '').strip()
    de = request.GET.get('de', '')
    ate = request.GET.get('ate', '')

    if tipo:
        qs = qs.filter(tipo_atividade=tipo)
    if q:
        qs = qs.filter(
            Q(usuario__username__icontains=q)
            | Q(usuario__email__icontains=q)
            | Q(descricao_resumida__icontains=q)
        )
    try:
        if de:
            qs = qs.filter(data_hora__date__gte=datetime.strptime(de, '%Y-%m-%d').date())
    except ValueError:
        de = ''
    try:
        if ate:
            qs = qs.filter(data_hora__date__lte=datetime.strptime(ate, '%Y-%m-%d').date())
    except ValueError:
        ate = ''

    qs = qs.order_by('-data_hora')
    paginator = Paginator(qs, 40)
    num_pagina = request.GET.get('pagina', 1)
    try:
        pagina_obj = paginator.page(num_pagina)
    except Exception:
        pagina_obj = paginator.page(1)

    context = {
        'secao': 'atividades',
        'atividades': pagina_obj,
        'paginas': _paginas(paginator, pagina_obj.number),
        'filtros': {'tipo': tipo, 'q': q, 'de': de, 'ate': ate},
        'tipos': UserActivityLog.TIPO_CHOICES,
        'tipos_icone': TIPO_ATIVIDADE_ICONES,
    }
    return render(request, 'painel_admin/atividades.html', context)


@painel_requerido
def trilhas(request, *args, **kwargs):
    qs = Trilha.objects.annotate(n_licoes=Count('licoes'))
    ativo = request.GET.get('ativo', '')
    if ativo in ('true', 'false'):
        qs = qs.filter(ativo=(ativo == 'true'))
    qs = qs.order_by('ordem')
    paginator = Paginator(qs, 30)
    pagina_obj = paginator.page(request.GET.get('pagina', 1))
    context = {
        'secao': 'conteudo',
        'subsecao': 'trilhas',
        'itens': pagina_obj,
        'paginas': _paginas(paginator, pagina_obj.number),
        'filtros': {'ativo': ativo},
    }
    return render(request, 'painel_admin/trilhas.html', context)


@painel_requerido
def licoes(request, *args, **kwargs):
    qs = (
        LicaoBiblica.objects
        .select_related('trilha')
        .annotate(n_exercicios=Count('exercicios'))
    )
    trilha_id = request.GET.get('trilha', '')
    area = request.GET.get('area', '')
    if trilha_id:
        qs = qs.filter(trilha_id=trilha_id)
    if area:
        qs = qs.filter(trilha__faixa_etaria=area)
    qs = qs.order_by('trilha__ordem', 'ordem')
    paginator = Paginator(qs, 30)
    pagina_obj = paginator.page(request.GET.get('pagina', 1))
    contexto_trilhas = Trilha.objects.order_by('ordem')
    context = {
        'secao': 'conteudo',
        'subsecao': 'licoes',
        'itens': pagina_obj,
        'paginas': _paginas(paginator, pagina_obj.number),
        'filtros': {'trilha': trilha_id, 'area': area},
        'trilhas_catalogo': contexto_trilhas,
        'areas': FAIXA_ETARIA_CHOICES,
    }
    return render(request, 'painel_admin/licoes.html', context)


@painel_requerido
def desafios(request, *args, **kwargs):
    qs = DesafioDiario.objects.annotate(
        concluidos=Count('desafiodiarioconcluido')
    ).order_by('-data')
    ativo = request.GET.get('ativo', '')
    if ativo in ('true', 'false'):
        qs = qs.filter(ativo=(ativo == 'true'))
    paginator = Paginator(qs, 30)
    pagina_obj = paginator.page(request.GET.get('pagina', 1))
    context = {
        'secao': 'conteudo',
        'subsecao': 'desafios',
        'itens': pagina_obj,
        'paginas': _paginas(paginator, pagina_obj.number),
        'filtros': {'ativo': ativo},
    }
    return render(request, 'painel_admin/desafios.html', context)


@painel_requerido
def recompensas(request, *args, **kwargs):
    qs = Recompensa.objects.annotate(
        desbloqueadas=Count('recompensausuario')
    ).order_by('-ativo', 'tipo', 'id')
    tipo = request.GET.get('tipo', '')
    if tipo:
        qs = qs.filter(tipo=tipo)
    paginator = Paginator(qs, 30)
    pagina_obj = paginator.page(request.GET.get('pagina', 1))
    context = {
        'secao': 'conteudo',
        'subsecao': 'recompensas',
        'itens': pagina_obj,
        'paginas': _paginas(paginator, pagina_obj.number),
        'filtros': {'tipo': tipo},
        'tipos': Recompensa.TIPO_CHOICES,
    }
    return render(request, 'painel_admin/recompensas.html', context)


@painel_requerido
def ranking(request, *args, **kwargs):
    """Ranking global e ligas semanais (estilo Duolingo)."""
    recalculado = False
    if request.GET.get('recalcular') == '1':
        calcular_ligas(forcar=True)
        recalculado = True
    semana = calcular_ligas()

    ligas = list(Liga.objects.order_by('ordem'))
    partes_semana = LigaParticipacao.objects.filter(semana=semana)

    contagem_qs = partes_semana.values('liga_id').annotate(n=Count('id'))
    contagem = {r['liga_id']: r['n'] for r in contagem_qs}

    kpi = {
        'participantes': partes_semana.count(),
        'promovidos': partes_semana.filter(promovido=True).count(),
        'rebaixados': partes_semana.filter(rebaixado=True).count(),
        'xp_semana': sum(xp_por_usuario(semana).values()),
        'semana_inicio': semana,
        'semana_fim': semana + timedelta(days=6),
    }

    liga_do_usuario = {
        p.usuario_id: p for p in partes_semana.select_related('liga')
    }

    usuarios_rank = list(
        User.objects.filter(is_active=True)
        .exclude(username__in=USUARIOS_ADMIN)
        .select_related('profile')
        .order_by('-profile__xp_total', 'username')
    )
    rows = []
    for i, u in enumerate(usuarios_rank, 1):
        part = liga_do_usuario.get(u.id)
        rows.append({
            'posicao': i,
            'user': u,
            'xp_total': u.profile.xp_total,
            'streak': u.profile.streak_atual,
            'nivel': u.profile.get_nivel_atual_display(),
            'liga': part.liga if part else None,
            'liga_posicao': part.posicao if part else None,
            'xp_semana': part.xp_semana if part else 0,
        })

    paginator = Paginator(rows, 25)
    num_pagina = request.GET.get('pagina', 1)
    try:
        pagina_obj = paginator.page(num_pagina)
    except Exception:
        pagina_obj = paginator.page(1)

    # Liga selecionada para exibir o detalhe
    liga_id = request.GET.get('liga', '')
    liga_selecionada = None
    if liga_id:
        liga_selecionada = get_object_or_404(Liga, id=liga_id)
    else:
        liga_selecionada = next(
            (l for l in ligas if contagem.get(l.id)), None
        )

    liga_membros = []
    if liga_selecionada:
        partes = list(
            LigaParticipacao.objects
            .filter(semana=semana, liga=liga_selecionada)
            .order_by('posicao')
        )
        usuarios_mapa = {
            u.id: u
            for u in User.objects
            .filter(id__in=[p.usuario_id for p in partes])
            .select_related('profile')
        }
        liga_membros = [
            {'part': p, 'user': usuarios_mapa.get(p.usuario_id)}
            for p in partes
        ]

    ligas_data = [
        {'liga': l, 'total': contagem.get(l.id, 0)} for l in ligas
    ]

    context = {
        'secao': 'ranking',
        'recalculado': recalculado,
        'kpi': kpi,
        'ligas_data': ligas_data,
        'liga_selecionada': liga_selecionada,
        'liga_membros': liga_membros,
        'rows': pagina_obj,
        'paginas': _paginas(paginator, pagina_obj.number),
        'total': paginator.count,
        'liga_filtro': liga_id,
    }
    return render(request, 'painel_admin/ranking.html', context)