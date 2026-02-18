from __future__ import annotations

from app.adapters.base import MarketAdapter
from app.adapters.kalshi import KalshiAdapter
from app.adapters.polymarket import PolymarketAdapter
from app.models import NormalizedMarket, Opportunity
from app.opportunity_engine import find_opportunities


class MonitorService:
    def __init__(self, adapters: list[MarketAdapter] | None = None):
        self.adapters = adapters or [PolymarketAdapter(), KalshiAdapter()]

    def get_market_snapshot(self) -> list[NormalizedMarket]:
        markets: list[NormalizedMarket] = []
        for adapter in self.adapters:
            markets.extend(adapter.fetch_markets())
        return markets

    def get_opportunities(self, min_spread: float = 0.03) -> list[Opportunity]:
        markets = self.get_market_snapshot()
        return find_opportunities(markets, min_spread=min_spread)
