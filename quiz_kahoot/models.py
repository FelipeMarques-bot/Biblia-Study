import string
import random
from django.db import models
from django.contrib.auth.models import User


def generate_pin():
    """Generate a random 6-digit PIN that is unique."""
    while True:
        pin = ''.join(random.choices(string.digits, k=6))
        if not QuizRoom.objects.filter(pin=pin, status__in=['lobby', 'question']).exists():
            return pin


NIVEL_CHOICES = [
    ('todos', 'Todos os níveis'),
    ('iniciante', 'Iniciante'),
    ('intermediario', 'Intermediário'),
    ('avancado', 'Avançado'),
    ('super_cristao', 'Super Cristão'),
]


class QuizRoom(models.Model):
    STATUS_CHOICES = [
        ('lobby', 'Aguardando'),
        ('question', 'Pergunta ativa'),
        ('results', 'Resultado da rodada'),
        ('finished', 'Encerrado'),
    ]

    pin = models.CharField(max_length=6, unique=True)
    host_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    host_session_key = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lobby')
    current_question_index = models.IntegerField(default=0)
    perguntas_total = models.IntegerField(default=10, help_text='Quantidade de perguntas escolhida pelo criador')
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='todos',
                             help_text='Nível das perguntas escolhido pelo criador')
    timer_seconds = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Quiz {self.pin} ({self.get_status_display()})'

    @property
    def total_questions(self):
        return self.questions.count()

    @property
    def players_list(self):
        return self.players.filter(is_host=False).order_by('-pontuacao')


class QuizPlayer(models.Model):
    room = models.ForeignKey(QuizRoom, on_delete=models.CASCADE, related_name='players')
    nome = models.CharField(max_length=50)
    pontuacao = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    is_host = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pontuacao', 'joined_at']

    def __str__(self):
        return f'{self.nome} ({self.room.pin}) - {self.pontuacao} pts'


class QuizQuestion(models.Model):
    room = models.ForeignKey(QuizRoom, on_delete=models.CASCADE, related_name='questions')
    exercicio_id = models.IntegerField(help_text='ID do exercício original')
    ordem = models.IntegerField(default=0)
    tipo = models.CharField(max_length=20)
    pergunta = models.TextField()
    opcoes = models.JSONField(default=list)
    correta_idx = models.IntegerField(default=0)
    dica = models.CharField(max_length=500, blank=True, default='')
    afirmativa = models.TextField(blank=True, default='')
    contexto = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f'#{self.ordem} {self.pergunta[:50]}'
