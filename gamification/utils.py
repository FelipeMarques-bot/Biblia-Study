from django.utils import timezone

from .models import UserActivityLog

def log_activity(usuario, tipo_atividade, descricao='', referencia='', xp_ganho=0):
    UserActivityLog.objects.create(
        usuario=usuario,
        tipo_atividade=tipo_atividade,
        descricao_resumida=descricao,
        referencia=referencia,
        xp_ganho=xp_ganho,
    )


def streak_efetivo(profile, persist=True):
    """Streak real considerando dias parados sem atividade.

    O valor salvo em ``streak_atual`` só é atualizado quando o usuário faz
    alguma atividade; se ele ficar dias sem fazer nada, o streak continua
    congelado. Esta função devolve o streak "vivo":

    - última atividade hoje ou ontem -> streak normal (o dia de hoje ainda
      pode ser completado para continuar a constância);
    - última atividade há 2+ dias -> constância quebrada -> 0.

    Quando ``persist`` é True, um pedido de leitura já zera o valor salvo
    para manter a exibição consistente em todo o app.
    """
    ultimo = profile.ultimo_dia_atividade
    if ultimo is None:
        return 0
    gap = (timezone.now().date() - ultimo).days
    if gap <= 1:
        return profile.streak_atual
    if persist and profile.streak_atual != 0:
        profile.streak_atual = 0
        profile.save(update_fields=['streak_atual', 'updated_at'])
    return 0
