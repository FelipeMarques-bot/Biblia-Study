import logging
from decouple import config

logger = logging.getLogger(__name__)

LLM_API_KEY = config('LLM_API_KEY', default='')
LLM_MODEL = config('LLM_MODEL', default='gemini-2.5-flash')

def _call_llm(prompt, temperature=0.3):
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        google_api_key=LLM_API_KEY,
        model=LLM_MODEL,
        temperature=temperature,
    )
    return llm.invoke(prompt).content.strip()

def gerar_dica_exercicio(exercicio, resposta_usuario=None):
    if not LLM_API_KEY:
        return gerar_dica_fallback(exercicio)

    try:
        prompt = f"""
Você é um tutor bíblico reformado. Dê uma dica curta e pastoral para este exercício:

Pergunta: {exercicio.enunciado}
Resposta do aluno: {resposta_usuario or 'N/A'}

Dica (máximo 2 frases, mencione a referência bíblica se aplicável):
"""
        return _call_llm(prompt, temperature=0.3)
    except Exception as e:
        logger.warning(f'Erro ao gerar dica com IA: {e}')
        return gerar_dica_fallback(exercicio)


def gerar_explicacao_licao(licao):
    if not LLM_API_KEY:
        return f'{licao.titulo}: {licao.resumo or licao.descricao}'

    try:
        prompt = f"""
Explique esta lição bíblica de forma simples e pastoral (máximo 4 frases):

Título: {licao.titulo}
Texto Base: {licao.texto_base}
Objetivo: {licao.objetivo}

Explicação centrada em Cristo, com aplicação prática:
"""
        return _call_llm(prompt, temperature=0.4)
    except Exception as e:
        logger.warning(f'Erro ao gerar explicação: {e}')
        return f'{licao.titulo}: {licao.resumo or licao.descricao}'


def gerar_devocional(tema, faixa_etaria='adulto', nivel='iniciante'):
    if not LLM_API_KEY:
        return gerar_devocional_fallback(tema)

    try:
        prompt = f"""
Crie um devocional bíblico curto (3-4 frases) para {faixa_etaria} sobre "{tema}".

Deve ser:
- Centrado em Deus e em Cristo
- Incluir uma referência bíblica
- Ter aplicação prática
- Tom pastoral e reformado

Devocional:
"""
        return _call_llm(prompt, temperature=0.5)
    except Exception as e:
        logger.warning(f'Erro ao gerar devocional: {e}')
        return gerar_devocional_fallback(tema)


def gerar_dica_fallback(exercicio):
    dados = exercicio.dados
    if exercicio.tipo == 'MULTIPLA_ESCOLHA' and 'dica' in dados:
        return dados['dica']
    return 'Leia o texto base com atenção e procure a resposta que melhor reflete o que a Bíblia ensina.'


def gerar_devocional_fallback(tema):
    devocionais = {
        'fé': 'A fé é confiança em Deus e na Sua Palavra. Hb 11:1 nos lembra que a fé é a certeza do que esperamos. Confie nas promessas de Deus hoje.',
        'gratidão': 'Em tudo dai graças (1Ts 5:18). A gratidão nos lembra que Deus é bom e cuida de nós. Hoje, agradeça a Deus por uma bênção específica.',
        'perdão': 'Assim como Cristo nos perdoou, somos chamados a perdoar (Cl 3:13). O perdão liberta quem perdoa. Ore por alguém que você precisa perdoar.',
        'oração': 'Não andeis ansiosos, mas em tudo pela oração apresentai vossos pedidos a Deus (Fp 4:6). Leve suas preocupações a Ele hoje.',
        'esperança': 'Bendito seja Deus que nos regenerou para uma viva esperança (1Pe 1:3). Nossa esperança está em Cristo, não nas circunstâncias.',
    }
    return devocionais.get(tema.lower(), f'Medite em {tema} à luz da Palavra de Deus hoje.')
