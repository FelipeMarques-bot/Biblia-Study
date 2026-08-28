# -*- coding: utf-8 -*-
"""Utilitarios do quiz: selecao de perguntas, limpeza de texto e contexto."""

# Correcoes de palavras com acentuacao/grafia faltante (tokens completos, de alta confianca).
CORRECOES = {
    # Palavras comuns muito usadas
    'nao': 'não', 'sao': 'são', 'ja': 'já', 'so': 'só', 'ate': 'até',
    'voce': 'você', 'tambem': 'também', 'ha': 'há', 'mes': 'mês',
    # Substantivos e verbos frequentes
    'tres': 'três', 'coracao': 'coração', 'leao': 'leão', 'leoes': 'leões',
    'mae': 'mãe', 'maos': 'mãos', 'oracao': 'oração', 'proibicao': 'proibição',
    'ameaca': 'ameaça', 'numero': 'número', 'historia': 'história', 'pagina': 'página',
    'biblia': 'Bíblia', 'cenaculo': 'cenáculo', 'ministerio': 'ministério',
    'pascoa': 'páscoa', 'ultima': 'última', 'ultimo': 'último', 'proximo': 'próximo',
    'esperanca': 'esperança', 'confianca': 'confiança', 'lancar': 'lançar',
    'crianca': 'criança', 'forca': 'força', 'praca': 'praça', 'protecao': 'proteção',
    'acao': 'ação', 'apos': 'após', 'vencera': 'vencerá',
    # Verbos no futuro
    'sera': 'será', 'fara': 'fará', 'podera': 'poderá', 'tera': 'terá', 'dara': 'dará',
    # Nomes proprios
    'joao': 'João', 'jose': 'José', 'moises': 'Moisés', 'gideao': 'Gideão',
}

# Entidades HTML comuns para normalizar o texto vindo dos dados.
ENTIDADES = {
    '&aacute;': 'á', '&eacute;': 'é', '&iacute;': 'í', '&oacute;': 'ó', '&uacute;': 'ú',
    '&atilde;': 'ã', '&otilde;': 'õ', '&ccedil;': 'ç', '&ntilde;': 'ñ', '&auml;': 'ä',
    '&nbsp;': ' ', '&quot;': '"', '&#39;': "'", '&apos;': "'", '&amp;': '&',
}


def limpar_texto(texto):
    """Limpa espacos, entidades HTML e corrige acentuacao/grafia de tokens conhecidos."""
    if not texto:
        return ''
    t = str(texto)
    for ent, val in ENTIDADES.items():
        t = t.replace(ent, val)
    # Remove marcacao markdown/asteriscos soltos e normaliza espacos
    t = t.replace('**', '').replace('__', '').replace('#', '')
    t = ' '.join(t.split())
    # Corrige tokens desprovidos de acento
    palavras = []
    for p in t.split(' '):
        palavras.append(_corrigir_tok(p))
    return ' '.join(palavras).strip()


def _corrigir_tok(tok):
    if not tok:
        return tok
    inicio = 0
    fim = len(tok)
    while inicio < fim and not tok[inicio].isalnum():
        inicio += 1
    while fim > inicio and not tok[fim - 1].isalnum():
        fim -= 1
    if inicio == fim:
        return tok
    nucleo = tok[inicio:fim]
    novo = CORRECOES.get(nucleo.lower())
    if novo is None:
        return tok
    if nucleo[0].isupper():
        novo = novo[0].upper() + novo[1:]
    return tok[:inicio] + novo + tok[fim:]


def contexto_para(exercicio):
    """Contexto da pergunta: referencia biblica da licao ou titulo da licao."""
    licao = exercicio.licao
    fonte = (getattr(licao, 'referencia', '') or '').strip() or (
        getattr(licao, 'titulo', '') or ''
    )
    return limpar_texto(fonte)


def payload_pergunta(pergunta, revelar=False):
    """Monta o dicionario da pergunta; correta_idx so quando `revelar`."""
    if pergunta is None:
        return None
    dados = {
        'pergunta': pergunta.pergunta,
        'opcoes': pergunta.opcoes,
        'tipo': pergunta.tipo,
        'afirmativa': pergunta.afirmativa,
        'ordem': pergunta.ordem,
        'contexto': pergunta.contexto,
    }
    if revelar:
        dados['correta_idx'] = pergunta.correta_idx
    return dados


def selecionar_perguntas(room):
    """Seleciona exercicios aleatorios para a sala e recria as perguntas do quiz."""
    from courses.models import Exercicio
    from .models import QuizQuestion

    total = getattr(room, 'perguntas_total', None) or 10
    total = max(5, min(20, int(total)))

    QuizQuestion.objects.filter(room=room).delete()

    exercicios = list(
        Exercicio.objects.filter(tipo__in=['MULTIPLA_ESCOLHA', 'VF'])
        .select_related('licao')
        .order_by('?')[:total]
    )

    for idx, ex in enumerate(exercicios):
        dados = ex.dados or {}

        if ex.tipo == 'VF':
            opcoes = [limpar_texto('Verdadeiro'), limpar_texto('Falso')]
            correta_idx = 0 if dados.get('resposta_correta', True) else 1
            afirmativa = limpar_texto(dados.get('afirmativa', ''))
        else:
            opcoes = [limpar_texto(a) for a in dados.get('alternativas', [])]
            correta_idx = int(dados.get('indice_correto', 0) or 0)
            afirmativa = ''

        QuizQuestion.objects.create(
            room=room,
            exercicio_id=ex.id,
            ordem=idx + 1,
            tipo=ex.tipo,
            pergunta=limpar_texto(ex.enunciado),
            opcoes=opcoes,
            correta_idx=correta_idx,
            dica=limpar_texto(dados.get('dica', '')),
            afirmativa=afirmativa,
            contexto=contexto_para(ex),
        )