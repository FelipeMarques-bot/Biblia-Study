"""
Base de conhecimento de teólogos para o bot devocional.
Cada teólogo tem frases organizadas por tópico para referência nas respostas.
"""

TEOLOGOS = {
    'agostinho': {
        'nome': 'Agostinho de Hipona',
        'epoca': '354-430',
        'linha': 'Pai da Graça',
        'frases': {
            'fe': [
                'A fé é crer o que ainda não vemos; a recompensa da fé é ver o que cremos. (Agostinho)',
                'Se compreendes, não é Deus. (Agostinho, Confissões)',
                'O coração inquieto só descansará em Ti, ó Deus. (Agostinho, Confissões III)',
            ],
            'graça': [
                'A graça não é recompensa de boas obras, mas o princípio delas. (Agostinho)',
                'Sem a graça de Deus, não podemos nem começar a querer o bem. (Agostinho)',
                'Deus não nos ordena o impossível antes de dar a graça. (Agostinho)',
            ],
            'pecado': [
                'O pecado é a palavra ou a obra contra a lei eterna. (Agostinho)',
                'A concupiscência é o inimigo contra o qual lutamos todos os dias. (Agostinho)',
                'Ninguém pode se purificar do pecado sem o perdão de Deus. (Agostinho)',
            ],
            'amor': [
                'Ama e faz o que quiseres. Se guardares o silêncio, guarda com amor; se falares, fala com amor; se corrigires, corrige com amor. (Agostinho)',
                'Tudo o que fazemos sem amor é vazio. (Agostinho)',
            ],
            'oracao': [
                'Orai como se tudo dependesse de Deus; trabalhai como se tudo dependesse de vós. (Agostinho)',
                'A oração é a chave para o dia e a tranqüilidade para a noite. (Agostinho)',
            ],
            'esperanca': [
                'A esperança tem dois filhos: a indignação e a coragem. A indignação com as coisas como são; a coragem para mudá-las. (Agostinho)',
            ],
        },
    },
    'lutero': {
        'nome': 'Martinho Lutero',
        'epoca': '1483-1546',
        'linha': 'Pai da Reforma',
        'frases': {
            'fe': [
                'A fé não é um assentimento vazio do intelecto, mas uma confiança viva e ousada do coração. (Lutero)',
                'A fé justificadora é uma confiança_Header cheia de certeza na graça de Deus. (Lutero)',
                'Somos justificados pela fé somente, sem as obras da lei. (Lutero, Romanos Comentário)',
            ],
            'graça': [
                'A graça de Deus é encontrada onde há sofrimento e cruz. (Lutero)',
                'Não somos justos pelas nossas obras, mas pela graça de Deus em Cristo. (Lutero)',
                'A graça é o início, o meio e o fim da nossa salvação. (Lutero)',
            ],
            'cruz': [
                'Deus não pode dar-nos a graça sem que nos humilhe primeiro. (Lutero)',
                'A cruz é o julgamento de Deus sobre a justiça humana. (Lutero)',
                'Quem não carrega sua cruz não pode ser meu discípulo. (Lutero, sobre Mc 8:34)',
            ],
            'biblia': [
                'A Bíblia é o bezerro de ouro dos teólogos. (Lutero)',
                'Sola Scriptura — Somente a Escritura é a autoridade suprema. (Lutero)',
                'Não aceito nem o papa nem os concílios, porque é evidente que erraram. Somente a Escritura me governa. (Lutero)',
            ],
            'liberdade': [
                'O cristão é um senhor livre de todos e servo de todos. (Lutero)',
                'A liberdade cristã é a liberdade de amar e servir. (Lutero)',
            ],
        },
    },
    'calvino': {
        'nome': 'João Calvino',
        'epoca': '1509-1564',
        'linha': 'Reforma Francesa',
        'frases': {
            'soberania': [
                'A soberania de Deus é a verdade mais consoladora para o crente. (Calvino)',
                'Deus governa todas as coisas commandos invioláveis. (Calvino, Institutas)',
                'Nada acontece no mundo sem o conselho determinado de Deus. (Calvino)',
            ],
            'graça': [
                'A graça de Deus é o único fundamento da nossa salvação. (Calvino)',
                'Deus nos elegeu em Cristo antes da fundação do mundo. (Calvino, Institutas III)',
                'A eleição é o eterno decreto de Deus, pelo qual determinou quem seria salvo. (Calvino)',
            ],
            'cristo': [
                'Cristo é o centro de toda a Escritura. (Calvino)',
                'Não há Deus nem Pai senão em Cristo. (Calvino)',
                'A cruz de Cristo é o centro da história da salvação. (Calvino)',
            ],
            'oracao': [
                'A oração é a conversa íntima do crente com Deus. (Calvino)',
                'Devemos orar sem cessar, porque sempre precisamos de Deus. (Calvino)',
            ],
            'santidade': [
                'Deus nos chama à santidade porque é santo. (Calvino)',
                'A santificação é a obra do Espírito Santo em nós. (Calvino)',
            ],
        },
    },
    'spurgeon': {
        'nome': 'Charles Haddon Spurgeon',
        'epoca': '1834-1892',
        'linha': 'Príncipe dos Pregadores',
        'frases': {
            'evangelho': [
                'O evangelho é bom demais para ser verdade, mas é verdadeiro demais para ser bom demais. (Spurgeon)',
                'O evangelho não é "faça", mas "feito". (Spurgeon)',
                'Se o teu religião não te dá nada melhor do que o que o mundo dá, desista dele. (Spurgeon)',
            ],
            'fe': [
                'A fé é a mão que recebe os presentes de Deus. (Spurgeon)',
                'Quanto mais fraco tu és, mais forte é a tua fé, porque depende mais de Deus. (Spurgeon)',
                'A fé não é Sentir, é Saber. (Spurgeon)',
            ],
            'tristeza': [
                'A tristeza do crente é temporária; a alegria do crente é eterna. (Spurgeon)',
                'Deus não nos Promete um dia sem tempestades, mas Promete o porto. (Spurgeon)',
            ],
            'esperanca': [
                'A esperança cristã é uma âncora da alma, segura e firme. (Spurgeon)',
                'Enquanto há vida, há esperança em Deus. (Spurgeon)',
            ],
            'oracao': [
                'A oração é a chave da manhã e a tranqüilidade da noite. (Spurgeon)',
                'Pouco pode ser feito sem oração; muito pode ser feito com ela. (Spurgeon)',
            ],
            'amor': [
                'O amor de Deus é o maior dos milagres. (Spurgeon)',
                'Quando não sabemos orar, o Espírito ora por nós. (Spurgeon)',
            ],
        },
    },
    'tozer': {
        'nome': 'A.W. Tozer',
        'epoca': '1897-1963',
        'linha': 'Profeta da devoção',
        'frases': {
            'deus': [
                'O que pensamos sobre Deus é a coisa mais importante de nós. (Tozer, O Conhecimento do Santo)',
                'Deus é tudo o queEleé, e nada do que nãoé. (Tozer)',
                'Deus não precisa de ouras provas da Sua existência;EleSe auto-revela. (Tozer)',
            ],
            'adoracao': [
                'A adoração é a Poeira da alma no salão do céu. (Tozer)',
                'A adoração é o único ato humano que não será eterno. (Tozer)',
                'Quebrar o primeiro mandamento é a pior idolatria. (Tozer)',
            ],
            'espirito': [
                'O Espírito Santo não é uma doutrina, é uma Pessoa. (Tozer)',
                'A plenitude do Espírito não é para uns poucos, é para todos. (Tozer)',
            ],
            'descanso': [
                'Deus não quer que você tenha ansiedade;Elequer que você tenha confiança. (Tozer)',
                'O cristão mais feliz é aquele que mais confia em Deus. (Tozer)',
            ],
        },
    },
    'lewis': {
        'nome': 'C.S. Lewis',
        'epoca': '1898-1963',
        'linha': 'Apologista cristão',
        'frases': {
            'cristo': [
                'O cristianismo, se falso, não tem importância; se verdadeiro, tem importância infinita. A única coisa que não pode é ser moderadamente importante. (Lewis)',
                'Ora, o Cristo que morreu pelos nossos pecados não pode ser meramente um grande mestre. Um homem que dissesse as coisas que Jesus disse não seria um grande mestre — seria um lunático. (Lewis)',
            ],
            'raciocinio': [
                'Eu acredito no cristianismo tão firmemente quanto acredito que a geometria euclidiana é verdadeira. (Lewis)',
                'Se Deus existisse, seria impossível provarSugeriuou refutá-Lo apenas com a razão. (Lewis)',
            ],
            'problemas': [
                'Deus sussurra aos nossos ouvidos na nossa prosperidade, grita na nossa dor. É Seu megafone para o surdo mundo. (Lewis, A Dor)',
                'A dor é o mensageiro de Deus para chamar a nossa atenção. (Lewis)',
            ],
            'moralidade': [
                'A moralidade cristã é como um mapa: não nos diz se estamos ou não no caminho, mas mostra onde está o caminho. (Lewis)',
                'Você não pode voltar atrás. Mas você pode começar de novo. (Lewis)',
            ],
            'conhecimento': [
                'Não háKnowledge semHumildade. (Lewis)',
                'A experiência é a professora mais cruel, porque faz o teste primeiro e a explicação depois. (Lewis)',
            ],
        },
    },
    'bonhoeffer': {
        'nome': 'Dietrich Bonhoeffer',
        'epoca': '1906-1945',
        'linha': 'Teólogo do discipulado',
        'frases': {
            'cruz': [
                'Quando Cristo chama um homem, Ele o chama para morrer. (Bonhoeffer, O Custo do Discipulado)',
                'A graça barata é a graça sem discipulado. (Bonhoeffer)',
                'Só crê de verdade quem obedece. (Bonhoeffer)',
            ],
            'comunidade': [
                'O cristão não é um idealista, é um crente. (Bonhoeffer)',
                'A comunidade cristã não é uma ideia, é uma realidade viva. (Bonhoeffer)',
            ],
            'oracao': [
                'A oração não é um meio de逃避da realidade, mas de enfrentá-la. (Bonhoeffer)',
                'Quem reza, não pode Odiar. (Bonhoeffer)',
            ],
            'amor': [
                'O amor pelo irmão é a prova do amor por Deus. (Bonhoeffer)',
                'Só quem ama é capaz de obedecer. (Bonhoeffer)',
            ],
        },
    },
    'machado': {
        'nome': 'Oswaldo Machado',
        'epoca': '1917-2015',
        'linha': 'Teólogo brasileiro',
        'frases': {
            'graça': [
                'A graça de Deus não nos livra do sofrimento, mas nos dá forças para enfrentá-lo. (Machado)',
                'Deus é justo para perdoar e misericordioso para restaurar. (Machado)',
            ],
            'esperanca': [
                'A esperança cristã não é otimismo; é certeza baseada nas promessas de Deus. (Machado)',
            ],
        },
    },
    'schaeffer': {
        'nome': 'Francis Schaeffer',
        'epoca': '1912-1984',
        'linha': 'Apologista cultural',
        'frases': {
            'cultura': [
                'O cristão deve ser um artefato vivo da verdade. (Schaeffer)',
                'Deus não é apenas o Deus dos indivíduos, mas também das nações. (Schaeffer)',
            ],
            'fe': [
                'A fé bíblica é uma fé que pensa. (Schaeffer)',
                'A verdade cristã é relevante para toda a vida. (Schaeffer)',
            ],
        },
    },
    'keller': {
        'nome': 'Timothy Keller',
        'epoca': '1950-2023',
        'linha': 'Pastor e apologista',
        'frases': {
            'graça': [
                'O evangelho não é um conceito para aceitar; é uma história para entrar. (Keller)',
                'A graça nos torna humildes porque não dependemos dos nossos méritos. (Keller)',
            ],
            'justificacao': [
                'A justificação é um veredicto declarativo, não um processo. (Keller)',
                'Somos aceitos por Deus não por nossas obras, mas pela obra de Cristo. (Keller)',
            ],
            'cidade': [
                'Deus não enviou seus melhores soldados para proteger a cidade, mas seus melhores amantes para servi-la. (Keller)',
            ],
            'justica': [
                'O evangelho é a justiça de Deus e a misericórdia de Deus se encontrando na cruz. (Keller)',
            ],
        },
    },
}


TOPICOS_KEYWORDS = {
    'fe': ['fé', 'crer', 'crença', 'confiança', 'acreditar', 'fé', 'falar', 'fé em deus', ' fé'],
    'graça': ['graça', 'perdão', 'perdoar', 'misericórdia', 'salvação', 'salvo', 'justificação', 'justificado'],
    'pecado': ['pecado', 'pecar', 'culpa', 'culpado', 'arrependimento', 'arrepender', 'transgressão'],
    'amor': ['amor', 'amar', 'caridade', 'bondade', 'compaixão', 'misericórdia'],
    'oracao': ['oração', 'orar', 'rezar', 'pedir a deus', 'comunicar com deus', 'intercessão'],
    'esperanca': ['esperança', 'esperar', 'futuro', 'eternidade', 'céu', 'vida eterna'],
    'cruz': ['cruz', 'sofrimento', 'dor', 'provação', 'tribulação', 'sofrer', 'carga'],
    'cristo': ['jesus', 'cristo', 'messias', 'salvador', 'filho de deus', 'encarnação'],
    'evangelho': ['evangelho', 'mensagem', 'boas novas', 'pregação', 'testemunho'],
    'deus': ['deus', 'pai', 'soberania', 'poder', 'onipotente', 'santidade'],
    'espirito': ['espírito santo', 'espírito', 'pentecostes', 'dons', 'carismas'],
    'comunidade': ['igreja', 'comunidade', 'irmãos', 'congregação', 'reunião'],
    'biblia': ['bíblia', 'escritura', 'palavra de deus', 'estudo bíblico', 'leitura'],
    'cultura': ['cultura', 'sociedade', 'mundo', 'contemporâneo', 'atual'],
    'adoracao': ['adoração', 'louvor', 'culto', 'música', 'hino'],
    'justica': ['justiça', 'social', 'igualdade', 'opressão', 'libertação'],
}


def buscar_teologo(topico, excluir=None):
    """Busca frases de teólogos sobre um tópico específico."""
    resultados = []
    excluir = excluir or []

    for chave, dados in TEOLOGOS.items():
        if chave in excluir:
            continue
        frases_topico = dados['frases'].get(topico, [])
        for frase in frases_topico:
            resultados.append({
                'teologo': dados['nome'],
                'epoca': dados['epoca'],
                'linha': dados['linha'],
                'frase': frase,
            })

    import random
    random.shuffle(resultados)
    return resultados[:3]


def detectar_topicos(texto):
    """Detecta tópicos relevantes no texto do usuário."""
    texto_lower = texto.lower()
    topicos_encontrados = []

    for topico, keywords in TOPICOS_KEYWORDS.items():
        for kw in keywords:
            if kw in texto_lower:
                topicos_encontrados.append(topico)
                break

    if not topicos_encontrados:
        topicos_encontrados = ['fe', 'esperanca']

    return topicos_encontrados


def formatar_resposta_teologos(topicos, excluir=None):
    """Formata uma resposta com referências de teólogos."""
    citacoes = []
    for topico in topicos[:2]:
        frases = buscar_teologo(topico, excluir)
        citacoes.extend(frases)

    if not citacoes:
        return ""

    texto = "\n\n📚 **Referências teológicas:**\n"
    for c in citacoes[:3]:
        texto += f"• {c['frase']}\n"

    return texto


# Categorias de conversa para o bot
CATEGORIAS_CONVERSA = {
    'devocional': {
        'nome': 'Devocional',
        'icone': '📖',
        'prompt_sistema': 'Você é um pastor devocional que fala de forma pastoral e amorosa. Use referências bíblicas e de teólogos quando relevante.',
    },
    'estudo': {
        'nome': 'Estudo Bíblico',
        'icone': '📚',
        'prompt_sistema': 'Você é um professor de estudo bíblico que explica passagens de forma clara e profunda. Cite versículos e teólogos.',
    },
    'oracao': {
        'nome': 'Oração',
        'icone': '🙏',
        'prompt_sistema': 'Você é um guia de oração que ajuda o usuário a orar. Sugira pedidos e agradeça a Deus.',
    },
    'conselho': {
        'nome': 'Conselho Pastoral',
        'icone': '💬',
        'prompt_sistema': 'Você é um conselheiro pastoral que oferece conselhos baseados na Bíblia. Seja compassivo e sábio.',
    },
    'teologia': {
        'nome': 'Teologia',
        'icone': '🎓',
        'prompt_sistema': 'Você é um teólogo que responde perguntas doutrinárias. Cite teólogos históricos como Agostinho, Lutero, Calvino, Spurgeon, Lewis, Bonhoeffer.',
    },
}
