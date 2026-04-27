"""Rotas HTTP para gerenciamento de despesas."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, ValidationError

from app.models.despesas import AtualizarDespesa, BuscarDespesa, CriarDespesa, FormaPagamento
from app.repositories.despesas_repository import Despesa, DespesaRepository

router = APIRouter(prefix="/despesas", tags=["despesas"])
_repository = DespesaRepository()


class DespesaResponse(BaseModel):
    """Representacao de despesa retornada pela API."""

    id: UUID
    descricao: str
    valor: Decimal
    data_transacao: date
    categoria: str
    forma_pagamento: FormaPagamento


class PaginacaoResponse(BaseModel):
    total: int
    limit: int
    offset: int
    has_next: bool


class ListarDespesasResponse(BaseModel):
    items: list[DespesaResponse]
    paginacao: PaginacaoResponse


def _safe_validation_errors(exc: ValidationError) -> list[dict[str, object]]:
    safe_errors: list[dict[str, object]] = []
    for error in exc.errors():
        safe_errors.append(
            {
                "loc": error.get("loc"),
                "msg": error.get("msg"),
                "type": error.get("type"),
            }
        )
    return safe_errors


def get_repository() -> DespesaRepository:
    """Retorna instancia do repositorio de despesas."""
    return _repository


def _to_response(despesa: Despesa) -> DespesaResponse:
    return DespesaResponse(
        id=despesa.id,
        descricao=despesa.descricao,
        valor=despesa.valor,
        data_transacao=despesa.data_transacao,
        categoria=despesa.categoria,
        forma_pagamento=despesa.forma_pagamento,
    )


@router.post("", response_model=DespesaResponse, status_code=status.HTTP_201_CREATED)
def criar_despesa(
    payload: CriarDespesa, repository: DespesaRepository = Depends(get_repository)
) -> DespesaResponse:
    despesa = repository.create(payload)
    return _to_response(despesa)


@router.get("", response_model=ListarDespesasResponse, status_code=status.HTTP_200_OK)
def listar_despesas(
    id: UUID | None = None,
    forma_pagamento: FormaPagamento | None = None,
    categoria: str | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    repository: DespesaRepository = Depends(get_repository),
) -> ListarDespesasResponse:
    try:
        filtros = BuscarDespesa(
            id=id,
            forma_pagamento=forma_pagamento,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim,
            limit=limit,
            offset=offset,
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=_safe_validation_errors(exc),
        ) from exc

    despesas = repository.list(filtros)
    total = repository.count(filtros)
    return ListarDespesasResponse(
        items=[_to_response(despesa) for despesa in despesas],
        paginacao=PaginacaoResponse(
            total=total,
            limit=limit,
            offset=offset,
            has_next=(offset + len(despesas)) < total,
        ),
    )


@router.get("/{despesa_id}", response_model=DespesaResponse, status_code=status.HTTP_200_OK)
def buscar_despesa_por_id(
    despesa_id: UUID, repository: DespesaRepository = Depends(get_repository)
) -> DespesaResponse:
    despesa = repository.get_by_id(despesa_id)
    if despesa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="despesa nao encontrada")
    return _to_response(despesa)


@router.put("/{despesa_id}", response_model=DespesaResponse, status_code=status.HTTP_200_OK)
def atualizar_despesa(
    despesa_id: UUID,
    payload: AtualizarDespesa,
    repository: DespesaRepository = Depends(get_repository),
) -> DespesaResponse:
    despesa_atualizada = repository.update(despesa_id, payload)
    if despesa_atualizada is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="despesa nao encontrada")
    return _to_response(despesa_atualizada)


@router.delete("/{despesa_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_despesa(
    despesa_id: UUID, repository: DespesaRepository = Depends(get_repository)
) -> Response:
    removida = repository.delete(despesa_id)
    if not removida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="despesa nao encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
