import json
import random
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import DesafioDiario, DesafioDiarioConcluido, Recompensa, RecompensaUsuario, SerieOuroDesafio, SerieOuroProgresso
from .utils import log_activity

VERSICULOS_DIARIOS = [
    {'versiculo': 'Filipenses 4:13', 'pergunta': 'Como a força de Cristo se manifesta na sua vida diária?'},
    {'versiculo': 'Jeremias 29:11', 'pergunta': 'Que planos você acredita que Deus tem para você?'},
    {'versiculo': 'Romanos 8:28', 'pergunta': 'Como você enxerga o propósito de Deus nas dificuldades?'},
    {'versiculo': 'Salmos 23:1', 'pergunta': 'O que significa para você o Senhor ser seu pastor?'},
    {'versiculo': 'Provérbios 3:5-6', 'pergunta': 'Em que áreas da sua vida é difícil confiar totalmente em Deus?'},
    {'versiculo': 'Isaías 41:10', 'pergunta': 'Quando você mais sente a presença de Deus em meio ao medo?'},
    {'versiculo': 'Mateus 11:28', 'pergunta': 'O que significa descansar em Cristo nos dias cansativos?'},
    {'versiculo': '2 Timóteo 1:7', 'pergunta': 'Como o Espírito de Deus ajuda você a enfrentar desafios?'},
    {'versiculo': 'Hebreus 11:1', 'pergunta': 'Como você descreve a sua fé hoje?'},
    {'versiculo': 'Efésios 2:8-9', 'pergunta': 'Como a graça de Deus transforma a forma como você vive?'},
    {'versiculo': '1 Coríntios 10:13', 'pergunta': 'De que forma Deus provê saída nas suas tentações?'},
    {'versiculo': 'João 3:16', 'pergunta': 'O que o amor de Deus significa para o seu dia a dia?'},
    {'versiculo': 'Mateus 6:33', 'pergunta': 'Como você busca primeiro o reino de Deus na prática?'},
    {'versiculo': 'Salmo 119:105', 'pergunta': 'De que forma a Palavra de Deus guia suas decisões?'},
]


@login_required
def desafio_diario_view(request):
    hoje = timezone.now().date()
    v = random.choice(VERSICULOS_DIARIOS)
    desafio, created = DesafioDiario.objects.get_or_create(
        data=hoje,
        defaults={
            'titulo': 'Desafio do Dia',
            'descricao': 'Leia o versículo abaixo e reflita sobre como ele se aplica à sua vida.',
            'versiculo': v['versiculo'],
            'pergunta': v['pergunta'],
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
        'recompensas': json.dumps(recompensas_data),
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
        'desafios_data': json.dumps(desafios_data),
        'user_xp': profile.xp_total,
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
