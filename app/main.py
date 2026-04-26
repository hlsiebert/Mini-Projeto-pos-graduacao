from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

from app.api.routes import router as despesas_router


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


app = FastAPI(title="Gerenciador de Despesas API")
app.include_router(despesas_router)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))
