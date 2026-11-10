# Bah: Plataforma de Inovação de Caxias do Sul

Plataforma web que **reúne as iniciativas do ecossistema de inovação de Caxias do Sul** (eventos, programas, capacitações, oportunidades de investimento e networking) num só lugar. Empreendedores encontram o que precisam de acordo com a etapa da sua jornada.

As iniciativas são organizadas em etapas da jornada empreendedora:

- **Buscar conhecimento**
- **Conexões**
- **Conseguir fundos**
- **Capacidades**
- **Operar e escalar**

Elas podem ser encontradas por uma **busca inteligente** que entende o significado do texto pesquisado, e não só as palavras exatas.

Projeto desenvolvido na **AGES (Agência Experimental de Engenharia de Software) da PUCRS** no 2º semestre de 2025 (agosto a novembro).

## Estrutura do repositório

Este repositório junta os dois repositórios originais do projeto, com o histórico de commits preservado:

| Pasta | Descrição | Stack |
|---|---|---|
| [`backend/`](backend) | API REST com autenticação, gestão de iniciativas, organizadores, tags e usuários, e busca híbrida | Python 3.12, FastAPI, SQLAlchemy, Alembic, PostgreSQL + pgvector, Sentence Transformers |
| [`frontend/`](frontend) | Site público e painel administrativo | TypeScript, React 19, Vite, Tailwind CSS v4, shadcn/ui, TanStack Query, Cypress |

## Funcionalidades

- **Página inicial** com a jornada empreendedora e as iniciativas em destaque.
- **Busca de iniciativas** por categoria, palavras-chave ou data.
- **Página da iniciativa** com descrição, local, horários, organizador, contato e link.
- **Painel administrativo** com login para cadastrar e editar iniciativas, organizadores e usuários.

## Busca híbrida

A busca combina dois métodos:

- **Busca textual** (*full-text search* do PostgreSQL);
- **Busca semântica**: as descrições das iniciativas são transformadas em vetores (*embeddings*) com Sentence Transformers e armazenadas com **pgvector**.

Os dois rankings são unidos com **Reciprocal Rank Fusion (RRF)**. Assim, a busca encontra iniciativas relevantes mesmo quando o texto pesquisado não tem as mesmas palavras da descrição.

## Arquitetura

- **Backend:** Clean Architecture em camadas `Routes` → `Controllers` → `Services` → `Repositories`, com validação via Pydantic e migrations com Alembic. Os testes usam pytest com banco isolado via Testcontainers.
- **Frontend:** SPA em React com componentes shadcn/ui, design system próprio (tokens de cores e tipografia do Bah) e testes E2E com Cypress.
- **CI/CD:** pipelines no GitLab CI (lint, testes e deploy), com o backend em Docker numa instância EC2.

## Como rodar

**Backend** (requer Docker):

```sh
cd backend
docker compose up --build
docker compose run --rm migrate   # aplica as migrations
docker compose run --rm seed      # popula dados iniciais
# Documentação da API: http://localhost:8000/docs
```

**Frontend** (requer Node.js >= 18):

```sh
cd frontend
npm install
npm run dev   # http://localhost:5173
```

Os READMEs de [`backend/`](backend) e [`frontend/`](frontend) têm mais detalhes (pipenv, testes, qualidade de código, banco de dados).

## Branches

A branch `main` tem o estado final de cada repositório (branch `dev` original). As demais branches originais foram mantidas com o nome da pasta como prefixo, por exemplo `backend/main` e `frontend/main`.

---

Repositórios originais: [tools.ages.pucrs.br/bah-plataforma-de-inova-o-de-caxias-do-sul](https://tools.ages.pucrs.br/bah-plataforma-de-inova-o-de-caxias-do-sul)
