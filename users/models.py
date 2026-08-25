from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

FAIXA_ETARIA_CHOICES = [
    ('crianca', 'Criança (7–12)'),
    ('adolescente', 'Adolescente (13–17)'),
    ('adulto', 'Adulto (18+)'),
]

NIVEL_CHOICES = [
    ('iniciante', 'Iniciante'),
    ('intermediario', 'Intermediário'),
    ('avancado', 'Avançado'),
    ('mestre', 'Mestre'),
]

NIVEL_THRESHOLDS = {
    'iniciante': 0,
    'intermediario': 1000,
    'avancado': 5000,
    'mestre': 15000,
}

NIVEL_ORDER = ['iniciante', 'intermediario', 'avancado', 'mestre']


class UserProfile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    faixa_etaria = models.CharField(max_length=20, choices=FAIXA_ETARIA_CHOICES, default='adulto')
    nivel_atual = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='iniciante')
    xp_total = models.IntegerField(default=0)
    pontos_para_ajuda = models.IntegerField(default=10)
    streak_atual = models.IntegerField(default=0)
    ultimo_dia_atividade = models.DateField(null=True, blank=True)
    nivel = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.get_faixa_etaria_display()}'

    def xp_para_proximo_nivel(self):
        return self.nivel * 500

    def progresso_nivel(self):
        return int((self.xp_total / self.xp_para_proximo_nivel()) * 100) if self.xp_para_proximo_nivel() > 0 else 0

    def calcular_nivel_automatico(self):
        """Calcula o nível baseado no XP total."""
        nivel = 'iniciante'
        for n in NIVEL_ORDER:
            if self.xp_total >= NIVEL_THRESHOLDS[n]:
                nivel = n
        return nivel

    def atualizar_nivel_se_necessario(self):
        """Atualiza o nível se o XP ultrapassou o threshold. Retorna True se houve mudança."""
        novo_nivel = self.calcular_nivel_automatico()
        if novo_nivel != self.nivel_atual:
            self.nivel_atual = novo_nivel
            self.save(update_fields=['nivel_atual', 'updated_at'])
            return True
        return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(usuario=instance)
