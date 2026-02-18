from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, Query

from app.service import MonitorService

app = FastAPI(title="Prediction Market Opportunity Monitor")
service = MonitorService()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/opportunities")
def opportunities(min_spread: float = Query(default=0.03, ge=0.0, le=1.0)) -> dict[str, list[dict]]:
    results = service.get_opportunities(min_spread=min_spread)
    return {"opportunities": [asdict(op) for op in results]}
