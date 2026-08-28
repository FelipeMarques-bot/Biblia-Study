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

ICON_EMOJI = {
    'open_in_new': '🚀', 'exit_to_app': '🚪', 'music_note': '🎵', 'book': '📖',
    'star': '⭐', 'church': '⛪', 'local_fire_department': '🔥', 'menu_book': '📚',
    'history_edu': '📜', 'school': '🎓', 'auto_stories': '📖', 'psychology': '🧠',
    'visibility': '👁️', 'volunteer_activism': '❤️', 'emoji_objects': '💡',
    'diversity_3': '🤝', 'gavel': '⚖️', 'workspace_premium': '🏆', 'groups': '👥',
    'psychology_alt': '🧠', 'sports_esports': '🎮', 'brush': '🎨', 'biotech': '🧬',
    'forest': '🌲', 'park': '🌿', 'water_drop': '💧', 'public': '🌍',
    'explore': '🧭', 'map': '🗺️', 'route': '🛤️', 'flag': '🚩', 'menu': '☰',
    'crown': '👑', 'warning': '⚠️', 'auto_awesome': '✨', 'balance': '⚖️',
    'forum': '💬', 'emoji_people': '👥', 'engineering': '🔧', 'vertical_align_top': '⬆️',
    'thumb_up': '👍', 'mail': '✉️', 'straighten': '📏', 'child_care': '👶',
    'child_friendly': '🧒', 'directions_walk': '🚶', 'emoji_events': '🏆',
}

@register.filter
def icone_emoji(nome):
    return ICON_EMOJI.get(nome, '📖')


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


NIVEL_LABELS_EXTRA = {
    'super_cristao': 'Super Cristão',
}


@register.filter
def nivel_label(valor):
    for v, l in NIVEL_CHOICES:
        if v == valor:
            return l
    return NIVEL_LABELS_EXTRA.get(valor, valor)


@register.filter
def faixa_label(valor):
    for v, l in FAIXA_ETARIA_CHOICES:
        if v == valor:
            return l
    return valor