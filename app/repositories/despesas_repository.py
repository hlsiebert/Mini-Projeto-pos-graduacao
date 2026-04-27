"""Repositorio SQLite para operacoes de despesas."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import UUID, uuid4

from app.models.despesas import AtualizarDespesa, BuscarDespesa, CriarDespesa


@dataclass(slots=True)
class Despesa:
    """Representa uma despesa persistida."""

    id: UUID
    descricao: str
    valor: Decimal
    data_transacao: date
    categoria: str
    forma_pagamento: str


class DespesaRepository:
    """Acesso a dados de despesas em SQLite."""

    def __init__(self, db_path: str = "app.db") -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS despesas (
                    id TEXT PRIMARY KEY,
                    descricao TEXT NOT NULL,
                    valor TEXT NOT NULL,
                    data_transacao TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    forma_pagamento TEXT NOT NULL
                )
                """
            )
            conn.commit()

    @staticmethod
    def _build_filtros_sql(filtros: BuscarDespesa) -> tuple[str, list[object]]:
        clauses: list[str] = []
        params: list[object] = []

        if filtros.id is not None:
            clauses.append("id = ?")
            params.append(str(filtros.id))
        if filtros.forma_pagamento is not None:
            clauses.append("forma_pagamento = ?")
            params.append(filtros.forma_pagamento.value)
        if filtros.categoria is not None:
            clauses.append("categoria = ?")
            params.append(filtros.categoria)
        if filtros.data_inicio is not None:
            clauses.append("data_transacao >= ?")
            params.append(filtros.data_inicio.isoformat())
        if filtros.data_fim is not None:
            clauses.append("data_transacao <= ?")
            params.append(filtros.data_fim.isoformat())

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        return where_sql, params

    @staticmethod
    def _row_to_despesa(row: sqlite3.Row) -> Despesa:
        return Despesa(
            id=UUID(row["id"]),
            descricao=str(row["descricao"]),
            valor=Decimal(str(row["valor"])),
            data_transacao=date.fromisoformat(str(row["data_transacao"])),
            categoria=str(row["categoria"]),
            forma_pagamento=str(row["forma_pagamento"]),
        )

    def create(self, payload: CriarDespesa) -> Despesa:
        despesa_id = uuid4()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO despesas (
                    id, descricao, valor, data_transacao, categoria, forma_pagamento
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(despesa_id),
                    payload.descricao,
                    str(payload.valor),
                    payload.data_transacao.isoformat(),
                    payload.categoria,
                    payload.forma_pagamento.value,
                ),
            )
            conn.commit()

        return Despesa(
            id=despesa_id,
            descricao=payload.descricao,
            valor=payload.valor,
            data_transacao=payload.data_transacao,
            categoria=payload.categoria,
            forma_pagamento=payload.forma_pagamento.value,
        )

    def list(self, filtros: BuscarDespesa | None = None) -> list[Despesa]:
        filtros = filtros or BuscarDespesa()
        where_sql, params = self._build_filtros_sql(filtros)
        sql = f"""
            SELECT id, descricao, valor, data_transacao, categoria, forma_pagamento
            FROM despesas
            {where_sql}
            ORDER BY data_transacao DESC, id DESC
            LIMIT ? OFFSET ?
        """
        params.extend([filtros.limit, filtros.offset])

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()

        return [self._row_to_despesa(row) for row in rows]

    def count(self, filtros: BuscarDespesa | None = None) -> int:
        filtros = filtros or BuscarDespesa()
        where_sql, params = self._build_filtros_sql(filtros)
        sql = f"""
            SELECT COUNT(*) AS total
            FROM despesas
            {where_sql}
        """
        with self._connect() as conn:
            row = conn.execute(sql, params).fetchone()
        return int(row["total"]) if row is not None else 0

    def get_by_id(self, despesa_id: UUID) -> Despesa | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT id, descricao, valor, data_transacao, categoria, forma_pagamento
                FROM despesas
                WHERE id = ?
                """,
                (str(despesa_id),),
            ).fetchone()

        if row is None:
            return None
        return self._row_to_despesa(row)

    def update(self, despesa_id: UUID, payload: AtualizarDespesa) -> Despesa | None:
        data = payload.model_dump(exclude_unset=True, exclude_none=True)
        if not data:
            return self.get_by_id(despesa_id)

        set_clauses: list[str] = []
        params: list[object] = []

        for key, value in data.items():
            set_clauses.append(f"{key} = ?")
            if isinstance(value, Decimal):
                params.append(str(value))
            elif isinstance(value, date):
                params.append(value.isoformat())
            elif hasattr(value, "value"):
                params.append(value.value)  # Enum
            else:
                params.append(value)

        params.append(str(despesa_id))

        with self._connect() as conn:
            cursor = conn.execute(
                f"UPDATE despesas SET {', '.join(set_clauses)} WHERE id = ?",
                params,
            )
            conn.commit()
            if cursor.rowcount == 0:
                return None

        return self.get_by_id(despesa_id)

    def delete(self, despesa_id: UUID) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM despesas WHERE id = ?", (str(despesa_id),))
            conn.commit()
            return cursor.rowcount > 0
