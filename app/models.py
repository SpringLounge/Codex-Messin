from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class NormalizedMarket:
    source: str
    market_id: str
    title: str
    canonical_id: str
    outcome: str
    yes_price: float
    no_price: float
    volume_24h: float
    liquidity: float
    close_time: datetime


@dataclass(frozen=True)
class Opportunity:
    canonical_id: str
    outcome: str
    buy_source: str
    sell_source: str
    buy_yes_price: float
    sell_yes_price: float
    gross_spread: float
    edge_score: float
