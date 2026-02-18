from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from urllib.error import URLError
from urllib.request import urlopen

from app.adapters.base import MarketAdapter
from app.models import NormalizedMarket


class KalshiAdapter(MarketAdapter):
    source = "kalshi"

    def __init__(self, endpoint: str | None = None, timeout_s: int = 5):
        self.endpoint = endpoint or "https://example.com/kalshi/markets"
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
            yes_price = float(item["yes_price"])
            normalized.append(
                NormalizedMarket(
                    source=self.source,
                    market_id=str(item["ticker"]),
                    title=item["title"],
                    canonical_id=item["canonical_id"],
                    outcome=item.get("outcome", "YES"),
                    yes_price=yes_price,
                    no_price=float(item.get("no_price", 1 - yes_price)),
                    volume_24h=float(item.get("volume_24h", 0.0)),
                    liquidity=float(item.get("open_interest", 0.0)),
                    close_time=datetime.fromisoformat(item["close_time"]),
                )
            )
        return normalized

    def _sample_data(self) -> list[NormalizedMarket]:
        now = datetime.now(timezone.utc)
        return [
            NormalizedMarket(
                source=self.source,
                market_id="KXBTC100K-26",
                title="Will BTC settle above $100k by 2026 year-end?",
                canonical_id="btc_above_100k_2026",
                outcome="YES",
                yes_price=0.46,
                no_price=0.54,
                volume_24h=1_900_000,
                liquidity=1_050_000,
                close_time=now + timedelta(days=300),
            ),
            NormalizedMarket(
                source=self.source,
                market_id="KXNYGOVX-26",
                title="Will candidate X win NY governor election 2026?",
                canonical_id="ny_governor_x_2026",
                outcome="YES",
                yes_price=0.49,
                no_price=0.51,
                volume_24h=620_000,
                liquidity=390_000,
                close_time=now + timedelta(days=240),
            ),
        ]
