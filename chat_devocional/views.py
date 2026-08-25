from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

from .models import SessaoDevocional, MensagemDevocional
from ia_engine.engine import gerar_resposta_chat, gerar_devocional
from ia_engine.devocionais import get_devocional_do_dia, get_historico_devocional


@login_required
def chat_view(request):
    """Pagina principal do chat devocional."""
    # Buscar sessao ativa
    sessao = SessaoDevocional.objects.filter(usuario=request.user).order_by('-data_inicio').first()

    mensagens = []
    devocional_hoje = get_devocional_do_dia()

    if sessao:
        mensagens = list(sessao.mensagens.values('remetente', 'texto', 'data_hora'))

    # Gerar devocional do dia para sidebar
    devocional_texto = gerar_devocional(devocional_hoje.get('titulo', 'fe'))

    # Topicos do chat
    categorias = [
        {'id': 'devocional', 'nome': 'Devocional', 'icon': '📖', 'desc': 'Meditacao diaria na Palavra'},
        {'id': 'estudo', 'nome': 'Estudo Biblico', 'icon': '📚', 'desc': 'Aprofunde seu conhecimento'},
        {'id': 'oracao', 'nome': 'Oracao', 'icon': '🙏', 'desc': 'Guia de oracao e intercessao'},
        {'id': 'conselho', 'nome': 'Conselho Pastoral', 'icon': '💛', 'desc': 'Acolhimento e orientacao'},
        {'id': 'teologia', 'nome': 'Teologia', 'icon': '🎓', 'desc': 'Doutrinas da fe reformada'},
    ]

    # Temas para o devocional
    temas = [
        {'id': 'fe', 'nome': 'Fe', 'icon': '✝️'},
        {'id': 'esperanca', 'nome': 'Esperanca', 'icon': '🌟'},
        {'id': 'gratidao', 'nome': 'Gratidao', 'icon': '🙏'},
        {'id': 'perdao', 'nome': 'Perdao', 'icon': '💫'},
        {'id': 'oracao', 'nome': 'Oracao', 'icon': '🕯️'},
        {'id': 'amor', 'nome': 'Amor', 'icon': '❤️'},
        {'id': 'cristo', 'nome': 'Cristo', 'icon': '👑'},
        {'id': 'familia', 'nome': 'Familia', 'icon': '👨‍👩‍👧‍👦'},
    ]

    # Historico de devocionais (ultimos 7 dias)
    historico_dev = get_historico_devocional(request.user, dias=7)

    context = {
        'sessao': sessao,
        'mensagens': mensagens,
        'devocional_hoje': devocional_hoje,
        'devocional_texto': devocional_texto,
        'categorias': json.dumps(categorias),
        'temas': json.dumps(temas),
        'historico_dev': historico_dev,
    }
    return render(request, 'chat.html', context)


@csrf_exempt
@login_required
def enviar_mensagem(request):
    """Envia mensagem e retorna resposta do bot."""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Metodo nao permitido'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON invalido'}, status=400)

    texto = data.get('mensagem', '').strip()
    sessao_id = data.get('sessao_id')
    categoria = data.get('categoria', 'devocional')
    tema = data.get('tema', 'fe')

    if not texto:
        return JsonResponse({'erro': 'Mensagem vazia'}, status=400)

    try:
        # Buscar ou criar sessao
        if sessao_id:
            sessao = get_object_or_404(SessaoDevocional, id=sessao_id, usuario=request.user)
        else:
            sessao = SessaoDevocional.objects.create(
                usuario=request.user,
                tema=tema,
            )

        # Salvar mensagem do usuario
        MensagemDevocional.objects.create(
            sessao=sessao,
            remetente='usuario',
            texto=texto,
        )

        # Construir historico
        historico = list(sessao.mensagens.values('remetente', 'texto'))
        historico_convertido = [{'tipo': m['remetente'], 'texto': m['texto']} for m in historico[-6:]]

        # Gerar resposta do bot
        resposta = gerar_resposta_chat(
            mensagem=texto,
            historico=historico_convertido,
            tema=tema,
            categoria=categoria,
        )

        # Salvar resposta do bot
        MensagemDevocional.objects.create(
            sessao=sessao,
            remetente='ia',
            texto=resposta,
        )

        return JsonResponse({
            'resposta': resposta,
            'sessao_id': sessao.id,
        })
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Erro ao enviar mensagem: {e}')
        return JsonResponse({
            'erro': str(e),
            'resposta': 'Desculpe, houve um erro ao processar sua mensagem. Por favor, tente novamente.',
        }, status=200)


@csrf_exempt
@login_required
def nova_sessao(request):
    """Cria uma nova sessao devocional."""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Metodo nao permitido'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}

    tema = data.get('tema', 'fe')
    categoria = data.get('categoria', 'devocional')

    sessao = SessaoDevocional.objects.create(
        usuario=request.user,
        tema=tema,
    )

    # Gerar devocional de boas-vindas
    devocional_hoje = get_devocional_do_dia()
    boas_vindas = (
        f"**📖 Devocional do Dia — {devocional_hoje['titulo']}**\n\n"
        f"**{devocional_hoje['passagem']}**\n\n"
    )
    if devocional_hoje.get('texto'):
        boas_vindas += f"*\"{devocional_hoje['texto']}\"*\n\n"
    boas_vindas += f"{devocional_hoje['reflexao']}\n\n"
    boas_vindas += f"🙏 **Oração:** {devocional_hoje['oracao']}\n\n"
    boas_vindas += f"---\n\n**Como posso te ajudar hoje?** Pode me perguntar sobre:\n"
    boas_vindas += "• Um versículo ou passagem bíblica\n"
    boas_vindas += "• Um tema da fé (fé, oração, amor, etc.)\n"
    boas_vindas += "• Uma dificuldade que enfrenta\n"
    boas_vindas += "• Uma doutrina da fé reformada"

    MensagemDevocional.objects.create(
        sessao=sessao,
        remetente='ia',
        texto=boas_vindas,
    )

    return JsonResponse({
        'sessao_id': sessao.id,
        'mensagem': boas_vindas,
    })


@login_required
def devocional_hoje(request):
    """Endpoint para pegar o devocional do dia."""
    dev = get_devocional_do_dia()
    return JsonResponse(dev)
