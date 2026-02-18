from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from urllib.error import URLError
from urllib.request import urlopen

from app.adapters.base import MarketAdapter
from app.models import NormalizedMarket


class PolymarketAdapter(MarketAdapter):
    source = "polymarket"

    def __init__(self, endpoint: str | None = None, timeout_s: int = 5):
        self.endpoint = endpoint or "https://example.com/polymarket/markets"
        self.timeout_s = timeout_s

    def fetch_markets(self) -> list[NormalizedMarket]:
        try:
            with urlopen(self.endpoint, timeout=self.timeout_s) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return self._normalize_payload(payload)
        except (URLError, TimeoutError, ValueError, KeyError):
            return self._sample_data()

    def _normalize_payload(self, payload: list[dict]) -> list[NormalizedMarket]:
        normalized: list[NormalizedMarket] = []
        for item in payload:
            normalized.append(
                NormalizedMarket(
                    source=self.source,
                    market_id=str(item["id"]),
                    title=item["title"],
                    canonical_id=item["canonical_id"],
                    outcome=item.get("outcome", "YES"),
                    yes_price=float(item["yes_price"]),
                    no_price=float(item.get("no_price", 1 - float(item["yes_price"]))),
                    volume_24h=float(item.get("volume_24h", 0.0)),
                    liquidity=float(item.get("liquidity", 0.0)),
                    close_time=datetime.fromisoformat(item["close_time"]),
                )
            )
        return normalized

    def _sample_data(self) -> list[NormalizedMarket]:
        now = datetime.now(timezone.utc)
        return [
            NormalizedMarket(
                source=self.source,
                market_id="poly-btc-2026",
                title="Will BTC close above 100k by Dec 31, 2026?",
                canonical_id="btc_above_100k_2026",
                outcome="YES",
                yes_price=0.41,
                no_price=0.59,
                volume_24h=2_300_000,
                liquidity=950_000,
                close_time=now + timedelta(days=300),
            ),
            NormalizedMarket(
                source=self.source,
                market_id="poly-election-ny-2026",
                title="Will candidate X win NY governor race 2026?",
                canonical_id="ny_governor_x_2026",
                outcome="YES",
                yes_price=0.52,
                no_price=0.48,
                volume_24h=740_000,
                liquidity=410_000,
                close_time=now + timedelta(days=240),
            ),
        ]
