# Gerenciador de Despesas API

Micro-API para gerenciamento de despesas pessoais, com separacao de gastos por **cartao de credito** e **debito**.

## Objetivo

Entregar um MVP de API REST para:

- registrar despesas pessoais
- classificar a forma de pagamento (`credito` ou `debito`)
- consultar gastos por periodo, categoria e tipo de pagamento
- apoiar a visualizacao de totais e acompanhamento financeiro basico

## Escopo do MVP

- cadastro de despesas
- listagem e filtro de despesas
- atualizacao e exclusao de despesas
- separacao de gastos por credito e debito
- validacoes basicas de dados de entrada

## Stack

- **Linguagem:** Python 3.11+
- **Framework API:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Validacao de dados:** Pydantic
- **Banco de dados (MVP):** SQLite
- **Testes:** Pytest

## Como rodar localmente

### 1) Clonar o repositorio

```bash
git clone <URL_DO_REPOSITORIO>
cd "Gerenciador de despesas"
```

### 2) Criar e ativar ambiente virtual

No Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Instalar dependencias

Se existir `requirements.txt`:

```bash
pip install -r requirements.txt
```

Caso ainda nao exista:

```bash
pip install fastapi uvicorn pydantic pytest python-dotenv
```

### 4) Configurar variaveis de ambiente

Copie o arquivo `.env.example` para `.env` e ajuste os valores locais:

```bash
cp .env.example .env
```

Variaveis disponiveis:

- `FRONTEND_ORIGINS`: origens permitidas no CORS, separadas por virgula.
  Exemplo: `http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174`
- `ALLOWED_HOSTS`: hosts permitidos pela API.
  Exemplo: `localhost,127.0.0.1,testserver`
- `LOG_LEVEL`: nivel de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

> O arquivo `.env` esta no `.gitignore` para evitar versionamento de dados sensiveis.

### 5) Subir a API

```bash
uvicorn app.main:app --reload
```

Documentacao interativa:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Roadmap de releases

### v0.1.0 - Base do MVP

- estrutura inicial do projeto
- endpoint de health-check
- CRUD de despesas
- separacao de transacoes por credito e debito
- persistencia local com SQLite

### v0.2.0 - Regras de negocio e consultas

- filtros por periodo, categoria e forma de pagamento
- calculo de total mensal por tipo (`credito`/`debito`)
- validacoes adicionais e tratamento de erros padronizado
- cobertura inicial de testes automatizados

### v0.3.0 - Qualidade e operacao

- paginacao em listagens
- logs estruturados
- ajustes de seguranca basica (CORS, cabecalhos, etc.)
- pipeline simples de CI para testes e lint

## Contrato de listagem (paginacao)

`GET /despesas` retorna:

```json
{
  "items": [
    {
      "id": "uuid",
      "descricao": "string",
      "valor": "10.50",
      "data_transacao": "2026-04-27",
      "categoria": "string",
      "forma_pagamento": "credito"
    }
  ],
  "paginacao": {
    "total": 1,
    "limit": 20,
    "offset": 0,
    "has_next": false
  }
}
```

## Qualidade (lint e testes)

```bash
ruff check .
pytest -q
```

O pipeline de CI roda automaticamente em push e pull request em `.github/workflows/ci.yml`.

### v1.0.0 - Release estavel

- documentacao consolidada da API
- melhoria de desempenho nos endpoints principais
- estrategia de versao da API (`/v1`)
- criterios minimos de observabilidade e monitoramento

## Proximos passos recomendados

- definir contrato dos endpoints (OpenAPI)
- adicionar migration tool (ex.: Alembic)
- preparar ambiente de homologacao
