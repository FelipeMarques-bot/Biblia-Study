import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class QuizConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer unificado para host e jogadores de uma sala."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pin = self.scope['url_route']['kwargs']['pin']
        self.room_group = f'quiz_{self.pin}'
        self.player_name = ''
        self.is_host = False

    async def connect(self):
        await self.channel_layer.group_add(self.room_group, self.channel_name)

        # Determinar nome e se é host via query string
        query = self.scope.get('query_string', b'').decode()
        params = dict(p.split('=') for p in query.split('&') if '=' in p)
        self.player_name = params.get('nome', 'Jogador')
        self.is_host = params.get('host', 'false') == 'true'

        await self.accept()

        # Adicionar jogador ao banco
        await self.add_player()

        # Notificar grupo que jogador entrou
        await self.channel_layer.group_send(self.room_group, {
            'type': 'player_joined',
            'nome': self.player_name,
            'players': await self.get_players(),
        })

    async def disconnect(self, close_code):
        await self.remove_player()
        await self.channel_layer.group_send(self.room_group, {
            'type': 'player_left',
            'nome': self.player_name,
            'players': await self.get_players(),
        })
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', '')

        if msg_type == 'start_game':
            await self.handle_start_game()
        elif msg_type == 'next_question':
            await self.handle_next_question()
        elif msg_type == 'submit_answer':
            await self.handle_submit_answer(data)
        elif msg_type == 'show_results':
            await self.handle_show_results()
        elif msg_type == 'restart':
            await self.handle_restart()
        elif msg_type == 'request_sync':
            await self.handle_sync()

    # === HANDLERS ===

    async def handle_start_game(self):
        if not self.is_host:
            return
        room = await self.get_room()
        if not room or room.status != 'lobby':
            return

        player_count = await self.get_player_count()
        if player_count < 1:
            await self.send(text_data=json.dumps({'type': 'error', 'msg': 'Necessário pelo menos 1 jogador'}))
            return

        await self.pick_questions(room)

        room.status = 'question'
        room.current_question_index = 0
        room.save()

        question = await self.get_current_question()
        players = await self.get_players()

        await self.channel_layer.group_send(self.room_group, {
            'type': 'game_started',
            'question': question,
            'total': await self.get_total_questions(),
            'players': players,
        })

    async def handle_next_question(self):
        if not self.is_host:
            return
        room = await self.get_room()
        if not room:
            return

        total = await self.get_total_questions()
        next_idx = room.current_question_index + 1

        if next_idx >= total:
            room.status = 'finished'
            room.finished_at = timezone.now()
            room.save()
            players = await self.get_players()
            await self.channel_layer.group_send(self.room_group, {
                'type': 'game_finished',
                'players': players,
            })
            return

        room.current_question_index = next_idx
        room.status = 'question'
        room.save()

        question = await self.get_current_question()
        players = await self.get_players()

        await self.channel_layer.group_send(self.room_group, {
            'type': 'new_question',
            'question': question,
            'question_index': next_idx,
            'total': total,
            'players': players,
        })

    async def handle_submit_answer(self, data):
        answer_idx = data.get('answer_idx')
        time_remaining = data.get('time_remaining', 0)

        room = await self.get_room()
        if not room or room.status != 'question':
            return

        result = await self.submit_answer_to_db(room, answer_idx, time_remaining)

        # Enviar resultado apenas para este jogador
        await self.send(text_data=json.dumps({
            'type': 'answer_result',
            **result,
        }))

        # Notificar grupo sobre resposta (para leaderboard)
        await self.channel_layer.group_send(self.room_group, {
            'type': 'player_answered',
            'nome': self.player_name,
            'players': await self.get_players(),
        })

    async def handle_show_results(self):
        if not self.is_host:
            return
        room = await self.get_room()
        if not room:
            return
        room.status = 'results'
        room.save()

        players = await self.get_players()
        await self.channel_layer.group_send(self.room_group, {
            'type': 'show_results',
            'players': players,
            'question': await self.get_current_question(revelar=True),
        })

    async def handle_restart(self):
        if not self.is_host:
            return
        room = await self.get_room()
        if not room:
            return

        await self.reset_game(room)

        players = await self.get_players()
        await self.channel_layer.group_send(self.room_group, {
            'type': 'game_restarted',
            'players': players,
        })

    async def handle_sync(self):
        """Envia estado atual da sala para quem pediu sync."""
        room = await self.get_room()
        if not room:
            return

        question = await self.get_current_question() if room.status == 'question' else None
        players = await self.get_players()

        await self.send(text_data=json.dumps({
            'type': 'sync_state',
            'status': room.status,
            'question': question,
            'question_index': room.current_question_index,
            'total': await self.get_total_questions(),
            'players': players,
            'timer': room.timer_seconds,
        }))

    # === GROUP MESSAGE HANDLERS ===

    async def player_joined(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_joined',
            'nome': event['nome'],
            'players': event['players'],
        }))

    async def player_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_left',
            'nome': event['nome'],
            'players': event['players'],
        }))

    async def game_started(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_started',
            'question': event['question'],
            'total': event['total'],
            'players': event['players'],
        }))

    async def new_question(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_question',
            'question': event['question'],
            'question_index': event['question_index'],
            'total': event['total'],
            'players': event['players'],
        }))

    async def player_answered(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_answered',
            'nome': event['nome'],
            'players': event['players'],
        }))

    async def show_results(self, event):
        payload = {
            'type': 'show_results',
            'players': event['players'],
        }
        if event.get('question'):
            payload['question'] = event['question']
        await self.send(text_data=json.dumps(payload))

    async def game_finished(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_finished',
            'players': event['players'],
        }))

    async def game_restarted(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_restarted',
            'players': event['players'],
        }))

    # === DB OPERATIONS ===

    @database_sync_to_async
    def get_room(self):
        from .models import QuizRoom
        try:
            return QuizRoom.objects.get(pin=self.pin)
        except QuizRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def add_player(self):
        from .models import QuizRoom, QuizPlayer
        try:
            room = QuizRoom.objects.get(pin=self.pin)
        except QuizRoom.DoesNotExist:
            return
        if self.is_host:
            QuizPlayer.objects.get_or_create(
                room=room, nome=self.player_name,
                defaults={'is_host': True}
            )
        else:
            QuizPlayer.objects.get_or_create(
                room=room, nome=self.player_name,
                defaults={'is_host': False}
            )

    @database_sync_to_async
    def remove_player(self):
        from .models import QuizPlayer
        QuizPlayer.objects.filter(
            room__pin=self.pin, nome=self.player_name
        ).delete()

    @database_sync_to_async
    def get_player_count(self):
        from .models import QuizPlayer
        return QuizPlayer.objects.filter(room__pin=self.pin, is_host=False).count()

    @database_sync_to_async
    def get_players(self):
        from .models import QuizPlayer
        players = QuizPlayer.objects.filter(room__pin=self.pin).order_by('-pontuacao', 'joined_at')
        return [
            {
                'nome': p.nome,
                'pontuacao': p.pontuacao,
                'streak': p.streak,
                'is_host': p.is_host,
            }
            for p in players
        ]

    @database_sync_to_async
    def get_current_question(self, revelar=False):
        from .models import QuizRoom
        from .quiz_utils import payload_pergunta
        try:
            room = QuizRoom.objects.get(pin=self.pin)
            q = room.questions.filter(ordem=room.current_question_index + 1).first()
            return payload_pergunta(q, revelar=revelar)
        except QuizRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def get_total_questions(self):
        from .models import QuizQuestion
        return QuizQuestion.objects.filter(room__pin=self.pin).count()

    @database_sync_to_async
    def submit_answer_to_db(self, room, answer_idx, time_remaining):
        from .models import QuizPlayer, QuizQuestion

        try:
            player = QuizPlayer.objects.get(room=room, nome=self.player_name)
        except QuizPlayer.DoesNotExist:
            return {'correct': False, 'points': 0, 'error': 'Jogador não encontrado'}

        question = QuizQuestion.objects.filter(room=room, ordem=room.current_question_index + 1).first()
        if not question:
            return {'correct': False, 'points': 0, 'error': 'Pergunta não encontrada'}

        correct = answer_idx == question.correta_idx

        base = 100 if correct else 0
        timer = room.timer_seconds
        time_bonus = int((time_remaining / timer) * 100) if correct and timer > 0 else 0

        if correct:
            player.streak += 1
            if player.streak > player.max_streak:
                player.max_streak = player.streak
        else:
            player.streak = 0

        streak_mult = min(2.0, 1.0 + max(0, player.streak - 1) * 0.1)
        points = int((base + time_bonus) * streak_mult)

        player.pontuacao += points
        player.save()

        return {
            'correct': correct,
            'points': points,
            'base': base,
            'time_bonus': time_bonus,
            'streak': player.streak,
            'streak_mult': round(streak_mult, 1),
            'total_pontuacao': player.pontuacao,
            'correct_answer': question.correta_idx,
        }

    @database_sync_to_async
    def pick_questions(self, room):
        from .quiz_utils import selecionar_perguntas
        selecionar_perguntas(room)

    @database_sync_to_async
    def reset_game(self, room):
        from .models import QuizPlayer, QuizQuestion
        QuizPlayer.objects.filter(room=room, is_host=False).update(
            pontuacao=0, streak=0, max_streak=0
        )
        QuizQuestion.objects.filter(room=room).delete()
        room.status = 'lobby'
        room.current_question_index = 0
        room.save()
