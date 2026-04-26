"""Modelos de entrada para operacoes de despesas."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FormaPagamento(str, Enum):
    """Forma de pagamento aceita pela API."""

    CREDITO = "credito"
    DEBITO = "debito"


class CriarDespesa(BaseModel):
    """Payload para criar uma despesa."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    descricao: str = Field(min_length=3, max_length=120)
    valor: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    data_transacao: date
    categoria: str = Field(min_length=2, max_length=50)
    forma_pagamento: FormaPagamento

    @field_validator("data_transacao")
    @classmethod
    def validar_data_transacao(cls, valor: date) -> date:
        """Impede data futura na transacao."""
        if valor > date.today():
            raise ValueError("data_transacao nao pode ser futura")
        return valor


class AtualizarDespesa(BaseModel):
    """Payload para atualizar uma despesa."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    descricao: str | None = Field(default=None, min_length=3, max_length=120)
    valor: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    data_transacao: date | None = None
    categoria: str | None = Field(default=None, min_length=2, max_length=50)
    forma_pagamento: FormaPagamento | None = None

    @field_validator("data_transacao")
    @classmethod
    def validar_data_transacao(cls, valor: date | None) -> date | None:
        """Impede data futura na transacao."""
        if valor is not None and valor > date.today():
            raise ValueError("data_transacao nao pode ser futura")
        return valor

    @model_validator(mode="after")
    def validar_campos_para_atualizacao(self) -> "AtualizarDespesa":
        """Exige ao menos um campo para atualizar."""
        if not any(
            (
                self.descricao is not None,
                self.valor is not None,
                self.data_transacao is not None,
                self.categoria is not None,
                self.forma_pagamento is not None,
            )
        ):
            raise ValueError("informe ao menos um campo para atualizacao")
        return self


class BuscarDespesa(BaseModel):
    """Filtros para buscar despesas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: UUID | None = None
    forma_pagamento: FormaPagamento | None = None
    categoria: str | None = Field(default=None, min_length=2, max_length=50)
    data_inicio: date | None = None
    data_fim: date | None = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validar_periodo(self) -> "BuscarDespesa":
        """Valida intervalo informado na busca."""
        if self.data_inicio and self.data_fim and self.data_inicio > self.data_fim:
            raise ValueError("data_inicio nao pode ser maior que data_fim")
        return self


class ApagarDespesa(BaseModel):
    """Identificador para apagar despesa."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
