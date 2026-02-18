# Prediction Market Opportunity Monitor (MVP)

A lightweight Python app that monitors event prices across prediction markets (starting with **Polymarket** and **Kalshi**) and surfaces potential opportunities.

## What this MVP does

- Pulls market snapshots from each exchange adapter.
- Normalizes markets into a shared schema.
- Groups markets by a shared `canonical_id`.
- Computes cross-market spreads and simple edge scores.
- Exposes a JSON API endpoint for opportunities.

## Project layout

- `app/models.py` – shared dataclasses for normalized markets.
- `app/adapters/` – exchange-specific clients + normalization.
- `app/opportunity_engine.py` – matching + opportunity detection logic.
- `app/service.py` – orchestration layer.
- `app/main.py` – FastAPI app (`/health` and `/opportunities`).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/opportunities`

## How to test the app

### 1) Run unit tests (logic-level)

```bash
pytest -q
```

This validates:
- spread/opportunity detection logic (`tests/test_opportunity_engine.py`)
- orchestration behavior across adapters (`tests/test_service.py`)

### 2) Smoke test the API locally

Start the app:

```bash
uvicorn app.main:app --reload
```

In a second shell, hit the endpoints:

```bash
curl -s http://127.0.0.1:8000/health
curl -s "http://127.0.0.1:8000/opportunities?min_spread=0.03"
```

Expected:
- `/health` returns `{"status":"ok"}`
- `/opportunities` returns JSON with an `opportunities` array.

### 3) Try different thresholds

```bash
curl -s "http://127.0.0.1:8000/opportunities?min_spread=0.10"
curl -s "http://127.0.0.1:8000/opportunities?min_spread=0.01"
```

Higher `min_spread` should produce fewer matches.

## Notes on real integrations

The provided adapters include HTTP fetch methods and deterministic fallback sample data to make local development/test reliable.

To productionize:
1. Fill in endpoint URLs/params based on current Polymarket and Kalshi APIs.
2. Add symbol/event mapping service to generate robust `canonical_id` values.
3. Add persistence, alerting (Slack/Telegram/email), and historical analytics.
4. Harden risk checks and fee/slippage modeling.
