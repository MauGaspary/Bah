# Bah: Plataforma de Inovação de Caxias do Sul

Plataforma web que **reúne as iniciativas do ecossistema de inovação de Caxias do Sul** (eventos, programas, capacitações, oportunidades de investimento e networking) num só lugar. Empreendedores encontram o que precisam de acordo com a etapa da sua jornada.

Caxias do Sul ocupa a 21ª posição no ranking nacional de inovação da ENAP. A cidade tem uma agenda ativa de eventos e uma forte cultura empreendedora, mas as iniciativas ficam dispersas e há pouca colaboração entre os atores do ecossistema. O Bah busca resolver isso com uma plataforma centralizada: uma agenda única de inovação que conecta empreendedores, instituições e programas de apoio.

As iniciativas são organizadas em etapas da jornada empreendedora:

- **Buscar conhecimento**
- **Conexões**
- **Conseguir fundos**
- **Capacidades**
- **Operar e escalar**

Elas podem ser encontradas por uma **busca inteligente** que entende o significado do texto pesquisado, e não só as palavras exatas.

Projeto desenvolvido na **AGES (Agência Experimental de Engenharia de Software) da PUCRS** no 2º semestre de 2025, em cinco sprints entre 6 de agosto e 19 de novembro.

## Estrutura do repositório

Este repositório junta os dois repositórios originais do projeto, com o histórico de commits preservado:

| Pasta | Descrição | Stack |
|---|---|---|
| [`backend/`](backend) | API REST com autenticação, gestão de iniciativas, organizadores, tags e usuários, e busca híbrida | Python 3.12, FastAPI, SQLAlchemy, Alembic, PostgreSQL + pgvector, Sentence Transformers |
| [`frontend/`](frontend) | Site público e painel administrativo | TypeScript, React 19, Vite, Tailwind CSS v4, shadcn/ui, TanStack Query, Cypress |

## Funcionalidades

- **Página inicial** com a jornada empreendedora e as iniciativas em destaque.
- **Busca de iniciativas** por categoria, palavras-chave ou data.
- **Calendário** com todas as iniciativas previstas.
- **Páginas institucionais:** Sobre nós, Nossos valores e Contato.
- **Página da iniciativa** com descrição, local, horários, organizador, contato e link.
- **Painel administrativo** com login para criar, editar, excluir e listar iniciativas, organizadores e usuários.

## Busca híbrida

A busca combina dois métodos:

- **Busca textual** (*full-text search* do PostgreSQL);
- **Busca semântica**: as descrições das iniciativas e os termos pesquisados são transformados em vetores (*embeddings*) com o modelo **multilingual-e5-base** (Sentence Transformers), e esses vetores são armazenados com **pgvector**. Por ser multilíngue, o modelo permite comparar buscas feitas em idiomas diferentes.

Os dois rankings são unidos com **Reciprocal Rank Fusion (RRF)**. Assim, a busca encontra iniciativas relevantes mesmo quando o texto pesquisado não tem as mesmas palavras da descrição.

## Arquitetura

- **Backend:** Clean Architecture em camadas `Routes` → `Controllers` → `Services` → `Repositories`, com validação via Pydantic e migrations com Alembic. Os testes usam pytest com banco isolado via Testcontainers.
- **Frontend:** SPA em React com componentes shadcn/ui, design system próprio (tokens de cores e tipografia do Bah) e testes E2E com Cypress.
- **Infraestrutura:** arquitetura cliente-servidor com Docker Compose. Os serviços são `db` (PostgreSQL 15), `migrate` (Alembic), `seed` e `app` (FastAPI).
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

## Equipe

**Professor orientador:** Daniel Antonio Callegari

| Nível | Integrantes |
|---|---|
| AGES I | Pedro Henrique de Oliveira Silveira, João Fabbrin Silveira, Rafael Jardim Sasso, João Vitor Araujo |
| AGES II | Matheus Corbellini Steindorff, Juliano Parmegiani Chies, Guilherme Oliveira Oliszewski, Gabriel Carreno Hoppe, Anthony Antonelli Andrade |
| AGES III | Lucas Pinto Vieira, Mauricio dos Santos Krziminski, Mauricio Pessoa de Mello Gaspary |
| AGES IV | Eduardo Pasqualotto Riboli, Guilherme Barreto, Jocemar Nicolodi Junior, João Vitor Schwingel, Marcelo Ferreira Boeira Júnior |

---

Repositórios originais e wiki: [tools.ages.pucrs.br/bah-plataforma-de-inova-o-de-caxias-do-sul](https://tools.ages.pucrs.br/bah-plataforma-de-inova-o-de-caxias-do-sul)
