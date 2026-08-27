# Plataforma Bíblica Gamificada

Interface premium para estudo bíblico gamificado que transforma devocionais diários em caminhos de aprendizado progressivo, combinando a progressão viciante de apps de idiomas com a calma visual de apps de bem-estar.

## Stack

| Camada   | Tecnologias                                      |
|----------|--------------------------------------------------|
| Backend  | Python + Django 5.2                              |
| Frontend | HTML + Tailwind CSS v3 + Alpine.js               |
| IA       | LangChain + OpenAI (com fallback sem API)        |
| Banco    | SQLite (dev) / PostgreSQL (prod)                 |
| Tarefas  | Celery + Redis (infra declarada)                 |
| Infra    | Docker + Gunicorn                                |

## Funcionalidades

- **Dashboard** — Streak diário, gráfico de XP semanal, próxima ação recomendada
- **Mapa de Trilhas** — Caminho vertical com nós ativos/bloqueados estilo Duolingo
- **Tela de Lição** — Quiz com múltipla escolha, V/F, associação, ordenação, barra de progresso e feedback visual
- **Tutor IA** — Dicas contextuais com consumo de pontos (LangChain)
- **Chat Devocional** — Reflexão guiada com IA em ambiente sereno
- **Série Ouro** — Desafios avançados com baús e animações premium
- **Gamificação** — XP, streak, níveis, recompensas e medalhas
- **Autenticação** — Cadastro por faixa etária e nível de conhecimento
- **Painel Admin Premium** — `/painel/` com dashboard de KPIs e gráficos, gestão completa de usuários (busca, filtros, detalhe, exportação CSV), feed de atividades e visão de conteúdo (trilhas, lições, desafios, recompensas). O acesso `admin/` redireciona para o painel.

## Conteúdo

Seed inicial com **12 trilhas, 44 lições, 130 exercícios** organizados por faixa etária e nível:

| Faixa Etária | Iniciante | Intermediário | Avançado |
|-------------|-----------|---------------|----------|
| Crianças    | 2 trilhas | Heróis da Fé | Parábolas de Jesus |
| Adolescentes| 2 trilhas | Vivendo a Fé | Discipulado e Chamado |
| Adultos     | 2 trilhas | Vida Cristã   | Doutrinas Centrais |

Execute `python seed_data.py` para popular o banco.

## Instalação Rápida

```bash
# Clone
git clone https://github.com/FelipeMarques-bot/plataforma-biblica.git
cd plataforma-biblica

# Backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env    # Configure sua SECRET_KEY
python manage.py migrate
python manage.py createsuperuser
python seed_data.py     # Popula conteúdo
python manage.py runserver

# Frontend (opcional, para build Tailwind)
npm install
npm run build
```

Acesse `http://127.0.0.1:8000`

## Docker

```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Estrutura do Projeto

```
plataforma-biblica/
├── core/                 # Configurações Django
├── users/                # Autenticação e perfil
├── courses/              # Trilhas, lições, exercícios
├── gamification/         # XP, streak, desafios, baús, activity log
├── ia_engine/            # LangChain (dicas, explicações, devocionais)
├── chat_devocional/      # Chat com IA
├── painel_admin/         # Painel administrativo premium (em /painel/)
├── templates/            # Templates Django
├── static/               # CSS e JS compilados
├── src/                  # Código fonte do frontend
├── seed_data.py          # Popula banco com conteúdo bíblico
├── PRD.md                # Documentação completa do produto
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

## Documentação

Veja [PRD.md](PRD.md) para a documentação completa do produto, incluindo:
- Sprints e checklists de desenvolvimento
- Diretrizes teológicas reformadas
- Guia de criação de conteúdo bíblico
- Especificações de gamificação e IA

## Licença

MIT — veja [LICENSE.txt](LICENSE.txt).
