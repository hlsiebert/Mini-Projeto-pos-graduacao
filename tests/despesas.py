from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.routes import get_repository
from app.main import app
from app.repositories.despesas_repository import DespesaRepository


@pytest.fixture
def repository() -> DespesaRepository:
    db_path = Path(f"test_{uuid4().hex}.db")
    repo = DespesaRepository(db_path=str(db_path))
    try:
        yield repo
    finally:
        if db_path.exists():
            try:
                db_path.unlink()
            except PermissionError:
                pass


@pytest.fixture
def client(repository: DespesaRepository) -> TestClient:
    app.dependency_overrides[get_repository] = lambda: repository
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def payload_despesa() -> dict[str, str | float]:
    return {
        "descricao": "Almoco executivo",
        "valor": 45.90,
        "data_transacao": str(date.today()),
        "categoria": "alimentacao",
        "forma_pagamento": "debito",
    }


def _criar_despesa(client: TestClient, payload: dict[str, str | float]) -> dict:
    response = client.post("/despesas", json=payload)
    assert response.status_code == 201
    return response.json()


def test_health_check_deve_retornar_status_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "timestamp" in body


def test_criar_despesa_deve_retornar_201_com_campos_preenchidos(
    client: TestClient, payload_despesa: dict[str, str | float]
) -> None:
    response = client.post("/despesas", json=payload_despesa)

    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["descricao"] == payload_despesa["descricao"]
    assert Decimal(body["valor"]) == Decimal("45.90")
    assert body["categoria"] == payload_despesa["categoria"]
    assert body["forma_pagamento"] == payload_despesa["forma_pagamento"]


def test_listar_despesas_deve_retornar_itens_criados_e_aceitar_filtro(
    client: TestClient, payload_despesa: dict[str, str | float]
) -> None:
    _criar_despesa(client, payload_despesa)
    _criar_despesa(
        client,
        {
            **payload_despesa,
            "descricao": "Streaming mensal",
            "categoria": "assinaturas",
            "forma_pagamento": "credito",
        },
    )

    response = client.get("/despesas", params={"forma_pagamento": "credito", "limit": 20, "offset": 0})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["descricao"] == "Streaming mensal"
    assert body[0]["forma_pagamento"] == "credito"


def test_buscar_despesa_por_id_deve_retornar_200_para_id_existente(
    client: TestClient, payload_despesa: dict[str, str | float]
) -> None:
    criada = _criar_despesa(client, payload_despesa)

    response = client.get(f"/despesas/{criada['id']}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == criada["id"]
    assert body["descricao"] == payload_despesa["descricao"]


def test_buscar_despesa_por_id_deve_retornar_404_para_id_inexistente(client: TestClient) -> None:
    response = client.get(f"/despesas/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "despesa nao encontrada"


def test_atualizar_despesa_deve_retornar_200_para_id_existente(
    client: TestClient, payload_despesa: dict[str, str | float]
) -> None:
    criada = _criar_despesa(client, payload_despesa)
    payload_atualizacao = {
        "descricao": "Almoco com cliente",
        "valor": 52.75,
        "forma_pagamento": "credito",
    }

    response = client.put(f"/despesas/{criada['id']}", json=payload_atualizacao)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == criada["id"]
    assert body["descricao"] == "Almoco com cliente"
    assert Decimal(body["valor"]) == Decimal("52.75")
    assert body["forma_pagamento"] == "credito"


def test_atualizar_despesa_deve_retornar_404_para_id_inexistente(
    client: TestClient, payload_despesa: dict[str, str | float]
) -> None:
    response = client.put(f"/despesas/{uuid4()}", json=payload_despesa)

    assert response.status_code == 404
    assert response.json()["detail"] == "despesa nao encontrada"


def test_apagar_despesa_deve_retornar_204_para_id_existente(
    client: TestClient, payload_despesa: dict[str, str | float]
) -> None:
    criada = _criar_despesa(client, payload_despesa)

    response = client.delete(f"/despesas/{criada['id']}")

    assert response.status_code == 204
    assert response.text == ""

    response_busca = client.get(f"/despesas/{criada['id']}")
    assert response_busca.status_code == 404


def test_apagar_despesa_deve_retornar_404_para_id_inexistente(client: TestClient) -> None:
    response = client.delete(f"/despesas/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "despesa nao encontrada"


def test_criar_despesa_deve_retornar_422_para_payload_invalido(client: TestClient) -> None:
    response = client.post(
        "/despesas",
        json={
            "descricao": "ab",
            "valor": 0,
            "data_transacao": str(date.today() + timedelta(days=1)),
            "categoria": "a",
            "forma_pagamento": "pix",
        },
    )

    assert response.status_code == 422


def test_listar_despesas_deve_retornar_500_para_periodo_invalido(client: TestClient) -> None:
    response = client.get(
        "/despesas",
        params={
            "data_inicio": "2026-04-27",
            "data_fim": "2026-04-01",
        },
    )

    assert response.status_code == 500


def test_atualizar_despesa_deve_retornar_422_quando_payload_vazio(
    client: TestClient, payload_despesa: dict[str, str | float]
) -> None:
    criada = _criar_despesa(client, payload_despesa)

    response = client.put(f"/despesas/{criada['id']}", json={})

    assert response.status_code == 422
