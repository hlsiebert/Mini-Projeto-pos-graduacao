# Backlog Minimo - MVP

## Release 1 - Core

- [ ] RF-01 - Cadastrar despesa (`POST /despesas`)
  - Criterios de aceite:
  - Payload aceita `descricao`, `valor`, `data_transacao`, `categoria`, `forma_pagamento`.
  - `forma_pagamento` aceita apenas `credito` ou `debito`.
  - Retorna `201` com `id` da despesa criada.

- [ ] RF-02 - Listar despesas (`GET /despesas`)
  - Criterios de aceite:
  - Retorna lista em JSON com despesas cadastradas.
  - Retorna `200` em consulta valida.

- [ ] RF-03 - Atualizar despesa (`PUT /despesas/{id}`)
  - Criterios de aceite:
  - Atualiza registro existente por `id`.
  - Retorna `200` com dados atualizados.
  - Retorna `404` para `id` inexistente.

- [ ] RF-04 - Excluir despesa (`DELETE /despesas/{id}`)
  - Criterios de aceite:
  - Remove registro existente por `id`.
  - Retorna `204` em exclusao bem-sucedida.
  - Retorna `404` para `id` inexistente.

- [ ] RF-05 - Health check (`GET /health`)
  - Criterios de aceite:
  - Retorna status operacional (`ok` ou equivalente).
  - Retorna timestamp da resposta.
  - Retorna `200`.

- [ ] RT-01 - Persistencia SQLite configurada
  - Criterios de aceite:
  - Dados de despesas permanecem apos reinicio da API.
  - Estrutura inicial de tabela criada para despesas.

- [ ] RT-02 - Validacao basica de payload
  - Criterios de aceite:
  - Campos obrigatorios nao aceitam ausencias.
  - Tipos invalidos retornam `422`.
  - Regras de negocio invalidas retornam `400`.

## Release 2 - Qualidade

- [ ] RF-06 - Filtro por forma de pagamento (`GET /despesas?forma_pagamento=`)
  - Criterios de aceite:
  - Filtra por `credito` ou `debito`.
  - Retorna apenas despesas compativeis com o filtro.
  - Retorna `200`.

- [ ] RF-07 - Filtro por periodo (`GET /despesas?data_inicio=&data_fim=`)
  - Criterios de aceite:
  - Filtra por intervalo de datas informado.
  - Intervalo invalido retorna `400`.
  - Retorna `200` para consulta valida.

- [ ] RF-08 - Filtro por categoria (`GET /despesas?categoria=`)
  - Criterios de aceite:
  - Retorna apenas despesas da categoria informada.
  - Retorna `200` para consulta valida.

- [ ] RF-09 - Consolidacao basica (`GET /despesas/consolidado`)
  - Criterios de aceite:
  - Retorna total por `forma_pagamento`.
  - Permite consolidar por periodo informado.
  - Retorna `200`.

- [ ] RT-03 - Padronizacao de respostas e erros HTTP
  - Criterios de aceite:
  - API utiliza codigos `200`, `201`, `204`, `400`, `404`, `422`, `500` conforme contrato.
  - Respostas de erro trazem mensagem clara e consistente.

- [ ] RT-04 - Cobertura minima de testes automatizados
  - Criterios de aceite:
  - Testes do endpoint `/health` implementados e passando.
  - Testes do fluxo CRUD principal implementados e passando.
  - Execucao de testes sem falhas no ambiente local.

- [ ] RT-05 - Logs minimos de aplicacao
  - Criterios de aceite:
  - Requisicoes e erros relevantes sao registrados.
  - Logs permitem rastrear falhas por endpoint.

## Release 3 - Entrega Final

- [ ] RT-06 - Documentacao OpenAPI e README alinhados
  - Criterios de aceite:
  - Swagger e ReDoc acessiveis em ambiente local.
  - README descreve como executar API e testes.
  - Endpoints documentados estao aderentes ao comportamento implementado.

- [ ] RT-07 - Execucao local padronizada
  - Criterios de aceite:
  - Projeto sobe via Uvicorn sem ajustes manuais extras.
  - Dependencias necessarias documentadas.
  - Passo a passo de setup validado em ambiente limpo.

- [ ] RT-08 - Checklist de pronto do MVP
  - Criterios de aceite:
  - CRUD e filtros essenciais funcionando.
  - Separacao por `credito` e `debito` validada.
  - Testes minimos passando.
  - Documentacao atualizada no repositorio.
