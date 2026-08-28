from django.db import models
from django.contrib.auth.models import User
from courses.models import LicaoBiblica, Trilha

LIGA_TIPO_CHOICES = [
    ('metal', 'Metal'),
    ('pedra', 'Pedra'),
]


class Liga(models.Model):
    """Liga semanal estilo Duolingo (metais e pedras preciosas)."""
    nome = models.CharField(max_length=50, unique=True)
    ordem = models.IntegerField(default=0, help_text='Ordem hierárquica (1 = Bronze)')
    tipo = models.CharField(max_length=20, choices=LIGA_TIPO_CHOICES, default='metal')
    icone = models.CharField(max_length=10, default='🥉')
    descricao = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Liga'
        verbose_name_plural = 'Ligas'

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'


class LigaParticipacao(models.Model):
    """Participação semanal do usuário em uma liga (snapshot p/ evolução)."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ligas')
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name='participacoes')
    semana = models.DateField(help_text='Segunda-feira da semana')
    posicao = models.IntegerField(default=0)
    xp_semana = models.IntegerField(default=0)
    promovido = models.BooleanField(default=False)
    rebaixado = models.BooleanField(default=False)
    liga_anterior = models.ForeignKey(
        Liga, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='+', help_text='Liga na semana anterior (para evolução)'
    )
    posicao_anterior = models.IntegerField(default=0)

    class Meta:
        ordering = ['semana', 'posicao']
        unique_together = ['usuario', 'semana']
        verbose_name = 'Participação em Liga'
        verbose_name_plural = 'Participações em Ligas'

    def __str__(self):
        return f'{self.usuario.username} - {self.liga.nome} (semana {self.semana})'


class DesafioDiario(models.Model):
    data = models.DateField(unique=True)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    versiculo = models.CharField(max_length=200, blank=True)
    pergunta = models.TextField(blank=True)
    xp_recompensa = models.IntegerField(default=30)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Desafio Diário'
        verbose_name_plural = 'Desafios Diários'

    def __str__(self):
        return f'{self.data} - {self.titulo}'


class DesafioDiarioConcluido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    desafio = models.ForeignKey(DesafioDiario, on_delete=models.CASCADE)
    concluido = models.BooleanField(default=True)
    data_conclusao = models.DateTimeField(auto_now_add=True)
    xp_ganho = models.IntegerField(default=0)

    class Meta:
        unique_together = ['usuario', 'desafio']

    def __str__(self):
        return f'{self.usuario.username} - {self.desafio.titulo}'


class Recompensa(models.Model):
    TIPO_CHOICES = [
        ('versiculo', 'Versículo'),
        ('medalha', 'Medalha'),
        ('curiosidade', 'Curiosidade'),
        ('xp_bonus', 'Bônus de XP'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='medalha')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    icone = models.CharField(max_length=50, default='🏅')
    xp_recompensa = models.IntegerField(default=100)
    criterio_licoes = models.IntegerField(default=0, help_text='Mínimo de lições concluídas')
    criterio_xp = models.IntegerField(default=0, help_text='XP mínimo')
    criterio_streak = models.IntegerField(default=0, help_text='Streak mínimo')
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recompensa'
        verbose_name_plural = 'Recompensas'

    def __str__(self):
        return f'{self.titulo} ({self.get_tipo_display()})'


class RecompensaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recompensas')
    recompensa = models.ForeignKey(Recompensa, on_delete=models.CASCADE)
    aberto = models.BooleanField(default=False)
    data_desbloqueio = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'recompensa']

    def __str__(self):
        return f'{self.usuario.username} - {self.recompensa.titulo}'


class SerieOuroDesafio(models.Model):
    licao = models.ForeignKey(LicaoBiblica, on_delete=models.SET_NULL, null=True, blank=True)
    trilha = models.ForeignKey(Trilha, on_delete=models.SET_NULL, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    faixa_etaria = models.CharField(max_length=20, default='adulto')
    nivel = models.CharField(max_length=20, default='avancado')
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    xp_recompensa = models.IntegerField(default=150)

    class Meta:
        verbose_name = 'Série Ouro - Desafio'
        verbose_name_plural = 'Série Ouro - Desafios'

    def __str__(self):
        return self.titulo


class SerieOuroExercicio(models.Model):
    desafio_ouro = models.ForeignKey(SerieOuroDesafio, on_delete=models.CASCADE, related_name='exercicios')
    tipo = models.CharField(max_length=20, choices=[
        ('MULTIPLA_ESCOLHA', 'Múltipla Escolha'),
        ('VF', 'Verdadeiro/Falso'),
        ('ASSOCIACAO', 'Associação'),
        ('ORDENACAO', 'Ordenação'),
    ], default='MULTIPLA_ESCOLHA')
    enunciado = models.TextField()
    dados = models.JSONField()
    peso_dificuldade = models.IntegerField(default=2)

    def __str__(self):
        return f'{self.desafio_ouro.titulo} - {self.enunciado[:50]}'


class SerieOuroProgresso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    desafio_ouro = models.ForeignKey(SerieOuroDesafio, on_delete=models.CASCADE)
    concluido = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    xp_ganho = models.IntegerField(default=0)
    pontos_para_ajuda_ganhos = models.IntegerField(default=0)

    class Meta:
        unique_together = ['usuario', 'desafio_ouro']

    def __str__(self):
        return f'{self.usuario.username} - {self.desafio_ouro.titulo}'


class UserActivityLog(models.Model):
    TIPO_CHOICES = [
        ('LICAO_CONCLUIDA', 'Lição Concluída'),
        ('DESAFIO_DIARIO', 'Desafio Diário'),
        ('SERIE_OURO', 'Série Ouro'),
        ('CHAT_DEVOCIONAL', 'Chat Devocional'),
        ('DICA_IA', 'Dica da IA'),
        ('EXPLICACAO_IA', 'Explicação da IA'),
        ('RECOMPENSA', 'Recompensa'),
        ('LOGIN', 'Login'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='atividades')
    tipo_atividade = models.CharField(max_length=30, choices=TIPO_CHOICES)
    referencia = models.CharField(max_length=200, blank=True, help_text='ID ou referência da atividade')
    descricao_resumida = models.TextField(blank=True)
    xp_ganho = models.IntegerField(default=0)
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Registro de Atividade'
        verbose_name_plural = 'Registros de Atividades'
        ordering = ['-data_hora']

    def __str__(self):
        return f'{self.usuario.username} - {self.get_tipo_atividade_display()} ({self.data_hora:%d/%m/%Y %H:%M})'
