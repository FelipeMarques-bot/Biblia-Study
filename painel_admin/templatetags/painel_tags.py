from django import template

from users.models import NIVEL_CHOICES, FAIXA_ETARIA_CHOICES
from gamification.models import UserActivityLog
from painel_admin.views import (
    NIVEL_STYLE,
    FAIXA_ICONE,
    TIPO_ATIVIDADE_ICONES,
    TIPO_ATIVIDADE_LABELS,
)

register = template.Library()


@register.filter
def nivel_style(valor):
    return NIVEL_STYLE.get(valor, NIVEL_STYLE['iniciante'])


@register.filter
def faixa_icone(valor):
    return FAIXA_ICONE.get(valor, '🧑')


@register.filter
def atividade_icon(tipo):
    return TIPO_ATIVIDADE_ICONES.get(tipo, '📌')


@register.filter
def atividade_label(tipo):
    return TIPO_ATIVIDADE_LABELS.get(tipo, tipo)


@register.filter
def nivel_label(valor):
    for v, l in NIVEL_CHOICES:
        if v == valor:
            return l
    return valor


@register.filter
def faixa_label(valor):
    for v, l in FAIXA_ETARIA_CHOICES:
        if v == valor:
            return l
    return valor