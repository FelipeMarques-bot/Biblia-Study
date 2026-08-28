import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse

from .models import QuizRoom, QuizPlayer, QuizQuestion, generate_pin, NIVEL_CHOICES
from .quiz_utils import payload_pergunta, selecionar_perguntas


def quiz_join(request):
    """Tela de entrada — digitar PIN para entrar ou criar sala."""
    if request.method == 'POST':
        pin = request.POST.get('pin', '').strip()
        nome = request.POST.get('nome', '').strip()
        action = request.POST.get('action', '')

        if action == 'create':
            return _create_room(request, nome)
        elif action == 'join' and pin:
            return _join_room(request, pin, nome)

    return render(request, 'quiz_join.html')


def _create_room(request, nome):
    """Cria uma nova sala e redireciona para o lobby como host."""
    if not nome:
        nome = 'Host'

    perguntas = request.POST.get('perguntas', '10') or '10'
    try:
        perguntas = int(perguntas)
    except (TypeError, ValueError):
        perguntas = 10
    perguntas = max(5, min(20, perguntas))

    nivel = request.POST.get('nivel', 'todos') or 'todos'
    niveis_validos = {n for n, _ in NIVEL_CHOICES}
    if nivel not in niveis_validos:
        nivel = 'todos'

    pin = generate_pin()
    room = QuizRoom.objects.create(
        pin=pin,
        perguntas_total=perguntas,
        nivel=nivel,
        host_session_key=request.session.session_key or '',
        host_user=request.user if request.user.is_authenticated else None,
    )

    # Host como jogador (marcado)
    QuizPlayer.objects.create(
        room=room,
        nome=nome,
        is_host=True,
    )

    request.session[f'quiz_host_{pin}'] = True
    request.session[f'quiz_nome_{pin}'] = nome

    return redirect('quiz_lobby', pin=pin)


def _join_room(request, pin, nome):
    """Entra em uma sala existente pelo PIN."""
    if not nome:
        nome = f'Jogador{random.randint(100,999)}'

    room = QuizRoom.objects.filter(pin=pin).first()
    if not room:
        return render(request, 'quiz_join.html', {'erro': 'Sala não encontrada. Verifique o PIN.'})

    if room.status not in ['lobby']:
        return render(request, 'quiz_join.html', {'erro': 'Esta sala já começou ou foi encerrada.'})

    # Verificar se já está na sala
    existing = QuizPlayer.objects.filter(room=room, nome=nome).first()
    if not existing:
        QuizPlayer.objects.create(room=room, nome=nome)

    request.session[f'quiz_nome_{pin}'] = nome
    return redirect('quiz_player', pin=pin)


def quiz_lobby(request, pin):
    """Sala de espera — jogadores aparecem em tempo real via WebSocket."""
    room = get_object_or_404(QuizRoom, pin=pin)
    is_host = request.session.get(f'quiz_host_{pin}', False)
    nome = request.session.get(f'quiz_nome_{pin}', '')

    return render(request, 'quiz_lobby.html', {
        'room': room,
        'pin': pin,
        'is_host': is_host,
        'nome': nome,
        'qr_url': request.build_absolute_uri(reverse('quiz_join')) + f'?pin={pin}',
    })


def quiz_host(request, pin):
    """Painel do host — controle do jogo com leaderboard."""
    room = get_object_or_404(QuizRoom, pin=pin)
    is_host = request.session.get(f'quiz_host_{pin}', False)

    if not is_host:
        return redirect('quiz_player', pin=pin)

    questions = room.questions.all()
    current_q = questions[room.current_question_index] if room.current_question_index < questions.count() else None

    return render(request, 'quiz_host.html', {
        'room': room,
        'pin': pin,
        'nome': request.session.get(f'quiz_nome_{pin}', ''),
        'questions': questions,
        'current_question': current_q,
        'total_questions': questions.count(),
    })


def quiz_player(request, pin):
    """Tela do jogador — responder perguntas com timer."""
    room = get_object_or_404(QuizRoom, pin=pin)
    nome = request.session.get(f'quiz_nome_{pin}', '')

    return render(request, 'quiz_player.html', {
        'room': room,
        'pin': pin,
        'nome': nome,
    })


def quiz_podium(request, pin):
    """Tela de pódium — resultado final."""
    room = get_object_or_404(QuizRoom, pin=pin)
    players = room.players.filter(is_host=False).order_by('-pontuacao')

    return render(request, 'quiz_podium.html', {
        'room': room,
        'pin': pin,
        'players': players,
        'podium': players[:3],
    })


def api_game_state(request, pin):
    """API: Estado completo da sala via REST (fallback p/ WebSocket indisponível)."""
    room = get_object_or_404(QuizRoom, pin=pin)
    players = list(
        room.players.order_by('-pontuacao', 'joined_at')
        .values('nome', 'pontuacao', 'streak', 'is_host')
    )

    question = None
    q = room.questions.filter(ordem=room.current_question_index + 1).first()
    if q:
        question = payload_pergunta(q, revelar=(room.status == 'results'))

    return JsonResponse({
        'status': room.status,
        'question': question,
        'question_index': room.current_question_index,
        'total': room.total_questions,
        'players': players,
        'timer': room.timer_seconds,
    })


def _pick_questions(room, quantity=10):
    """Seleciona perguntas para a sala (delegado ao utilitário compartilhado)."""
    selecionar_perguntas(room)


@require_POST
@csrf_exempt
def api_start_game(request, pin):
    """API: Iniciar o jogo — seleciona perguntas e muda status."""
    room = get_object_or_404(QuizRoom, pin=pin)

    # Verificar que é o host
    if not request.session.get(f'quiz_host_{pin}', False):
        return JsonResponse({'error': 'Apenas o host pode iniciar o jogo'}, status=403)

    if room.status != 'lobby':
        return JsonResponse({'error': 'Jogo já foi iniciado'}, status=400)

    player_count = room.players.filter(is_host=False).count()
    if player_count == 0:
        return JsonResponse({'error': 'Necessário pelo menos 1 jogador'}, status=400)

    # Selecionar perguntas (quantidade escolhida pelo criador da sala)
    selecionar_perguntas(room)

    room.status = 'question'
    room.current_question_index = 0
    room.save()

    return JsonResponse({'ok': True, 'total_questions': room.total_questions})


@require_POST
@csrf_exempt
def api_next_question(request, pin):
    """API: Avançar para próxima pergunta."""
    room = get_object_or_404(QuizRoom, pin=pin)

    if not request.session.get(f'quiz_host_{pin}', False):
        return JsonResponse({'error': 'Apenas o host pode avançar'}, status=403)

    total = room.total_questions
    next_idx = room.current_question_index + 1

    if next_idx >= total:
        room.status = 'finished'
        room.save()
        return JsonResponse({'finished': True})

    room.current_question_index = next_idx
    room.status = 'question'
    room.save()

    return JsonResponse({'ok': True, 'question_index': next_idx})


@require_POST
@csrf_exempt
def api_show_results(request, pin):
    """API: Mostrar resultado da rodada (antes de próxima pergunta)."""
    room = get_object_or_404(QuizRoom, pin=pin)

    if not request.session.get(f'quiz_host_{pin}', False):
        return JsonResponse({'error': 'Apenas o host'}, status=403)

    room.status = 'results'
    room.save()
    return JsonResponse({'ok': True})


@require_POST
@csrf_exempt
def api_submit_answer(request, pin):
    """API: Jogador envia resposta."""
    room = get_object_or_404(QuizRoom, pin=pin)
    data = __import__('json').loads(request.body)
    nome = data.get('nome', '')
    answer_idx = data.get('answer_idx')

    if not nome or answer_idx is None:
        return JsonResponse({'error': 'Dados incompletos'}, status=400)

    player = QuizPlayer.objects.filter(room=room, nome=nome).first()
    if not player:
        return JsonResponse({'error': 'Jogador não encontrado'}, status=404)

    total = room.total_questions
    if room.current_question_index >= total:
        return JsonResponse({'error': 'Jogo já encerrado'}, status=400)

    question = room.questions.filter(ordem=room.current_question_index + 1).first()
    if not question:
        return JsonResponse({'error': 'Pergunta não encontrada'}, status=404)

    correct = answer_idx == question.correta_idx

    # Calcular pontos
    base = 100 if correct else 0
    time_bonus = 0  # Será calculado pelo frontend baseado no tempo restante
    streak_mult = 1.0

    if correct:
        player.streak += 1
        if player.streak > player.max_streak:
            player.max_streak = player.streak
        streak_mult = min(2.0, 1.0 + (player.streak - 1) * 0.1)
    else:
        player.streak = 0

    # Frontend envia tempo_restante para calcular bônus
    time_remaining = data.get('time_remaining', 0)
    timer = room.timer_seconds
    time_bonus = int((time_remaining / timer) * 100) if correct and timer > 0 else 0

    points = int((base + time_bonus) * streak_mult)
    player.pontuacao += points
    player.save()

    return JsonResponse({
        'correct': correct,
        'points': points,
        'base': base,
        'time_bonus': time_bonus,
        'streak': player.streak,
        'streak_mult': round(streak_mult, 1),
        'total_pontuacao': player.pontuacao,
    })


@require_POST
@csrf_exempt
def api_restart(request, pin):
    """API: Reiniciar o jogo."""
    room = get_object_or_404(QuizRoom, pin=pin)

    if not request.session.get(f'quiz_host_{pin}', False):
        return JsonResponse({'error': 'Apenas o host'}, status=403)

    # Resetar jogadores
    room.players.filter(is_host=False).update(pontuacao=0, streak=0, max_streak=0)
    # Limpar perguntas
    room.questions.all().delete()
    room.status = 'lobby'
    room.current_question_index = 0
    room.save()

    return JsonResponse({'ok': True})
