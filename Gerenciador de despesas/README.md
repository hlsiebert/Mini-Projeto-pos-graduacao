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
pip install fastapi uvicorn pydantic pytest
```

### 4) Subir a API

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

### v1.0.0 - Release estavel

- documentacao consolidada da API
- melhoria de desempenho nos endpoints principais
- estrategia de versao da API (`/v1`)
- criterios minimos de observabilidade e monitoramento

## Proximos passos recomendados

- definir contrato dos endpoints (OpenAPI)
- adicionar migration tool (ex.: Alembic)
- preparar ambiente de homologacao

