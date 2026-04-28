# Gerenciador de Despesas API

Micro-API para gerenciamento de despesas pessoais, com separacao de gastos por cartao de credito e debito.

## Pre-requisitos

- Python **3.12.x** (recomendado) ou 3.11+
- Git
- (Opcional) `make` para usar os atalhos do `Makefile`

Validar versao do Python:

```bash
python --version
```

## Quickstart (maquina limpa)

```bash
git clone <URL_DO_REPOSITORIO>
cd "Gerenciador de despesas"
python -m venv .venv
```

Ativar ambiente virtual:

- Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

- Linux/macOS:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

Criar `.env`:

- Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

- Linux/macOS:

```bash
cp .env.example .env
```

Subir API:

```bash
python -m uvicorn app.main:app --reload
```

Validar que subiu corretamente:

- Health check: `http://127.0.0.1:8000/health` (esperado `200` com `{"status":"ok",...}`)
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Configuracao por ambiente (`.env`)

- `FRONTEND_ORIGINS`: origens permitidas no CORS (separadas por virgula)
- `ALLOWED_HOSTS`: hosts permitidos pela API
- `LOG_LEVEL`: nivel de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`)

Exemplo:

```env
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
LOG_LEVEL=INFO
```

## Banco de dados local (SQLite)

- O banco padrao e `app.db` na raiz do projeto.
- Se o arquivo nao existir, ele e criado automaticamente na primeira execucao da API.

## Comandos de desenvolvimento

Sem `make`:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
python -m ruff check .
python -m pytest -q
```

Com `make`:

```bash
make install
make run
make lint
make test
```

> No Windows, se `make` nao estiver instalado, use os comandos `python -m ...` acima.

## Endpoints (contrato tecnico)

### `GET /health`
- Retorna status da API.

### `POST /despesas`
- Cria despesa.

Exemplo de payload:

```json
{
  "descricao": "Almoco",
  "valor": 45.90,
  "data_transacao": "2026-04-28",
  "categoria": "alimentacao",
  "forma_pagamento": "debito"
}
```

### `GET /despesas`
- Lista despesas com filtros e paginacao.
- Query params: `id`, `forma_pagamento`, `categoria`, `data_inicio`, `data_fim`, `limit`, `offset`.

Exemplo de resposta:

```json
{
  "items": [
    {
      "id": "uuid",
      "descricao": "Almoco",
      "valor": "45.90",
      "data_transacao": "2026-04-28",
      "categoria": "alimentacao",
      "forma_pagamento": "debito"
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

### `GET /despesas/{id}`
- Busca despesa por ID.

### `PUT /despesas/{id}`
- Atualiza despesa por ID (parcial).

### `DELETE /despesas/{id}`
- Remove despesa por ID.

## Estrutura do projeto

```text
app/
  main.py                        # app FastAPI, middlewares, logs, seguranca
  api/routes.py                  # endpoints HTTP
  models/despesas.py             # schemas/validacoes Pydantic
  repositories/despesas_repository.py  # acesso SQLite
tests/
  despesas.py                    # suite de testes de API
.github/workflows/ci.yml         # pipeline CI (lint + testes)
Makefile                         # atalhos de desenvolvimento
```

## CI (GitHub Actions)

Pipeline em `.github/workflows/ci.yml`, executada em:

- `push` para `main`
- `pull_request` para `main`

Etapas:

1. instala dependencias
2. roda `ruff check .`
3. roda `pytest -q`

## Troubleshooting

- Erro de CORS no frontend:
  - confira `FRONTEND_ORIGINS` no `.env` e reinicie a API.
- Porta 8000 ocupada:
  - rode em outra porta: `python -m uvicorn app.main:app --reload --port 8001`.
- `ModuleNotFoundError`:
  - confirme venv ativo e rode `python -m pip install -r requirements.txt`.
- PowerShell bloqueando scripts:
  - ative venv via terminal com permissao adequada ou use terminal `cmd`.
- CI falhando em lint/teste:
  - execute localmente `python -m ruff check .` e `python -m pytest -q`.

## Contribuicao

Fluxo recomendado:

1. criar branch de feature/fix
2. implementar mudancas
3. rodar lint e testes localmente
4. abrir PR para `main`

Padrao de commit recomendado: Conventional Commits (ex.: `feat: ...`, `fix: ...`, `ci: ...`).
