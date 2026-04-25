# Escopo do MVP - Micro-API de Gerenciamento de Despesas

## 1. Objetivo

Definir e implementar um MVP de micro-API para controle de despesas pessoais, com foco em simplicidade operacional, separacao de gastos por forma de pagamento (`credito` e `debito`) e suporte a consultas basicas para acompanhamento financeiro individual.

## 2. Requisitos Funcionais

### RF-01 - Cadastro de despesa
A API deve permitir registrar uma despesa com os seguintes campos minimos:
- descricao
- valor
- data da transacao
- categoria
- forma de pagamento (`credito` ou `debito`)

### RF-02 - Listagem de despesas
A API deve permitir listar despesas cadastradas.

### RF-03 - Filtro por forma de pagamento
A API deve permitir filtrar despesas por `credito` ou `debito`.

### RF-04 - Filtro por periodo
A API deve permitir filtrar despesas por intervalo de datas (data inicial e data final).

### RF-05 - Filtro por categoria
A API deve permitir filtrar despesas por categoria.

### RF-06 - Atualizacao de despesa
A API deve permitir atualizar uma despesa existente por identificador unico.

### RF-07 - Exclusao de despesa
A API deve permitir remover uma despesa existente por identificador unico.

### RF-08 - Endpoint de saude
A API deve expor endpoint `GET /health` retornando status operacional e timestamp de resposta.

### RF-09 - Consolidacao basica
A API deve permitir consulta de totalizadores de despesas por:
- forma de pagamento (`credito`/`debito`)
- periodo informado

## 3. Requisitos Nao Funcionais

### RNF-01 - Tecnologia
Implementacao em Python 3.12 com FastAPI.

### RNF-02 - Formato de dados
API em JSON com validacao de payload de entrada e saida.

### RNF-03 - Contrato HTTP
Uso de codigos HTTP coerentes com a operacao:
- `200` para sucesso em consultas/atualizacoes
- `201` para criacao
- `400` para erro de validacao de regra
- `404` para recurso inexistente
- `422` para payload invalido
- `500` para erro interno nao tratado

### RNF-04 - Persistencia
Persistencia local inicial com SQLite para suporte ao MVP.

### RNF-05 - Observabilidade minima
Logs de requisicoes e erros em nivel aplicacao.

### RNF-06 - Testabilidade
Cobertura minima de testes automatizados para endpoint de saude e fluxo principal de despesas (CRUD basico).

### RNF-07 - Portabilidade local
Execucao local via ambiente virtual (`.venv`) e servidor Uvicorn.

### RNF-08 - Documentacao
Documentacao da API disponivel via OpenAPI (Swagger/ReDoc) e documentacao funcional minima no repositorio.

## 4. Fora do Escopo (MVP)

- autenticacao e autorizacao de usuarios
- multiusuario e controle de acesso por conta
- integracao com bancos, Open Finance ou operadoras de cartao
- conciliacao automatica de fatura
- parcelamento de compras e controle avancado de parcelas
- importacao de extratos (CSV/OFX) e exportacao de relatorios
- dashboards analiticos avancados e previsao financeira
- notificacoes (email, push, webhook)
- deploy produtivo com alta disponibilidade e escalabilidade horizontal

## 5. Criterios de Pronto do MVP

Para considerar o MVP pronto:
- endpoints principais implementados e funcionais
- validacoes basicas aplicadas para os campos obrigatorios
- separacao de gastos por credito/debito funcionando
- filtros essenciais operacionais (periodo, categoria, forma de pagamento)
- testes minimos executando com sucesso
- documentacao atualizada no repositorio
