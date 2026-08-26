from django.db import models
from django.contrib.auth.models import User

TIPO_EXERCICIO_CHOICES = [
    ('MULTIPLA_ESCOLHA', 'Múltipla Escolha'),
    ('VF', 'Verdadeiro/Falso'),
    ('ASSOCIACAO', 'Associação'),
    ('ORDENACAO', 'Ordenação'),
]

DIFICULDADE_CHOICES = [
    (1, 'Fácil'),
    (2, 'Médio'),
    (3, 'Difícil'),
    (4, 'Mestre'),
]

FAIXA_ETARIA_CHOICES = [
    ('crianca', 'Criança'),
    ('adolescente', 'Adolescente'),
    ('adulto', 'Adulto'),
]

class Trilha(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    faixa_etaria = models.CharField(max_length=20, choices=[
        ('crianca', 'Criança'), ('adolescente', 'Adolescente'), ('adulto', 'Adulto')
    ], default='adulto')
    nivel = models.CharField(max_length=20, choices=[
        ('iniciante', 'Iniciante'), ('intermediario', 'Intermediário'), ('avancado', 'Avançado')
    ], default='iniciante')
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    icone = models.CharField(max_length=30, default='📖')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Trilha'
        verbose_name_plural = 'Trilhas'

    def __str__(self):
        return f'{self.nome} ({self.get_faixa_etaria_display()} - {self.get_nivel_display()})'


class LicaoBiblica(models.Model):
    trilha = models.ForeignKey(Trilha, on_delete=models.CASCADE, related_name='licoes')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    texto_base = models.TextField(help_text='Texto ou referência bíblica')
    referencia = models.CharField(max_length=100, blank=True, help_text='Ex: Gênesis 1:1-31')
    objetivo = models.TextField(blank=True)
    resumo = models.TextField(blank=True)
    ordem = models.IntegerField(default=0)
    xp_recompensa = models.IntegerField(default=50)

    class Meta:
        ordering = ['trilha', 'ordem']
        verbose_name = 'Lição Bíblica'
        verbose_name_plural = 'Lições Bíblicas'

    def __str__(self):
        return f'{self.trilha.nome} - {self.titulo}'


class Exercicio(models.Model):
    licao = models.ForeignKey(LicaoBiblica, on_delete=models.CASCADE, related_name='exercicios')
    tipo = models.CharField(max_length=20, choices=TIPO_EXERCICIO_CHOICES, default='MULTIPLA_ESCOLHA')
    enunciado = models.TextField()
    dados = models.JSONField(help_text='JSON com alternativas, respostas etc.')
    peso_dificuldade = models.IntegerField(default=1)
    ordem = models.IntegerField(default=0)

    class Meta:
        ordering = ['licao', 'ordem']

    def __str__(self):
        return f'{self.licao.titulo} - {self.enunciado[:50]}'


class ProgressoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresso')
    licao = models.ForeignKey(LicaoBiblica, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    xp_ganho_sessao = models.IntegerField(default=0)
    respostas = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ['usuario', 'licao']
        verbose_name = 'Progresso do Usuário'
        verbose_name_plural = 'Progressos dos Usuários'

    def __str__(self):
        return f'{self.usuario.username} - {self.licao.titulo}'


class ExercisePool(models.Model):
    """Pool de exercícios para geração infinita de conteúdo."""
    TOPICO_CHOICES = [
        ('antigo_testamento', 'Antigo Testamento'),
        ('novo_testamento', 'Novo Testamento'),
        ('gospels', 'Evangelhos'),
        ('epistolas', 'Epístolas'),
        ('sabedoria', 'Livros de Sabedoria'),
        ('profecia', 'Profecia'),
        ('atos', 'Atos e História'),
        ('genesis', 'Gênesis'),
        ('exodo', 'Êxodo'),
        ('psalmos', 'Salmos'),
        ('proverbios', 'Provérbios'),
        ('isaias', 'Isaías'),
        ('mateus', 'Mateus'),
        ('joao', 'João'),
        ('romanos', 'Romanos'),
        ('efesios', 'Efésios'),
        ('hebreus', 'Hebreus'),
        ('revelacao', 'Apocalipse'),
    ]

    licao = models.ForeignKey(LicaoBiblica, on_delete=models.CASCADE, related_name='pool_exercicios', null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_EXERCICIO_CHOICES, default='MULTIPLA_ESCOLHA')
    topico = models.CharField(max_length=30, choices=TOPICO_CHOICES, default='novo_testamento')
    enunciado = models.TextField()
    dados = models.JSONField(help_text='JSON com alternativas, respostas etc.')
    dificuldade = models.IntegerField(choices=DIFICULDADE_CHOICES, default=1)
    faixa_etaria = models.CharField(max_length=20, choices=FAIXA_ETARIA_CHOICES, default='adulto')
    referencia_biblica = models.CharField(max_length=100, blank=True, help_text='Ex: João 3:16')
    ativo = models.BooleanField(default=True)
    criado_por_ia = models.BooleanField(default=False)
    peso_dificuldade = models.IntegerField(default=1)
    vezes_usado = models.IntegerField(default=0)
    taxa_acerto = models.FloatField(default=0.0, help_text='Taxa de acerto geral (0.0 a 1.0)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['dificuldade', 'topico']
        verbose_name = 'Exercício do Pool'
        verbose_name_plural = 'Pool de Exercícios'

    def __str__(self):
        return f'[{self.get_dificuldade_display()}] {self.enunciado[:60]}'


class PerformanceTracker(models.Model):
    """Rastreia performance do usuário por tópico e dificuldade."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performance_tracker')
    topico = models.CharField(max_length=30, choices=ExercisePool.TOPICO_CHOICES)
    dificuldade = models.IntegerField(choices=DIFICULDADE_CHOICES)
    total_questoes = models.IntegerField(default=0)
    acertos = models.IntegerField(default=0)
    erros = models.IntegerField(default=0)
    combo_maximo = models.IntegerField(default=0)
    combo_atual = models.IntegerField(default=0)
    ultima_questao_data = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['usuario', 'topico', 'dificuldade']
        verbose_name = 'Tracker de Performance'
        verbose_name_plural = 'Trackers de Performance'

    def __str__(self):
        return f'{self.usuario.username} - {self.topico} (D{self.dificuldade})'

    @property
    def taxa_acerto(self):
        if self.total_questoes == 0:
            return 0.0
        return self.acertos / self.total_questoes

    @property
    def deve_promover(self):
        """Promove se taxa de acerto > 80% e pelo menos 5 questões respondidas."""
        return self.total_questoes >= 5 and self.taxa_acerto > 0.8

    @property
    def deve_rebaixar(self):
        """Rebaixa se taxa de acerto < 30% e pelo menos 5 questões respondidas."""
        return self.total_questoes >= 5 and self.taxa_acerto < 0.3


class GeneratedLesson(models.Model):
    """Lição gerada por IA para conteúdo infinito."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='licoes_geradas')
    titulo = models.CharField(max_length=200)
    topico = models.CharField(max_length=30, choices=ExercisePool.TOPICO_CHOICES)
    dificuldade = models.IntegerField(choices=DIFICULDADE_CHOICES, default=1)
    referencia_biblica = models.CharField(max_length=100, blank=True)
    conteudo_gerado = models.TextField(help_text='Conteúdo da lição gerado por IA')
    exercicios_gerados = models.JSONField(default=list, help_text='Lista de exercícios gerados')
    xp_recompensa = models.IntegerField(default=50)
    concluida = models.BooleanField(default=False)
    xp_ganho = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Lição Gerada'
        verbose_name_plural = 'Lições Geradas'

    def __str__(self):
        return f'{self.usuario.username} - {self.titulo}'
