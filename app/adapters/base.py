from __future__ import annotations

from abc import ABC, abstractmethod

from app.models import NormalizedMarket


class MarketAdapter(ABC):
    source: str

    @abstractmethod
    def fetch_markets(self) -> list[NormalizedMarket]:
        """Return a normalized snapshot for this exchange."""
