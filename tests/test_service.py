from datetime import datetime, timedelta, timezone

from app.adapters.base import MarketAdapter
from app.models import NormalizedMarket
from app.service import MonitorService


class StubAdapter(MarketAdapter):
    def __init__(self, source: str, yes_price: float):
        self.source = source
        self.yes_price = yes_price

    def fetch_markets(self) -> list[NormalizedMarket]:
        return [
            NormalizedMarket(
                source=self.source,
                market_id=f"{self.source}-1",
                title="Event",
                canonical_id="event_1",
                outcome="YES",
                yes_price=self.yes_price,
                no_price=1 - self.yes_price,
                volume_24h=500_000,
                liquidity=500_000,
                close_time=datetime.now(timezone.utc) + timedelta(days=7),
            )
        ]


def test_monitor_service_collects_from_all_adapters():
    service = MonitorService(adapters=[StubAdapter("polymarket", 0.35), StubAdapter("kalshi", 0.44)])

    snapshot = service.get_market_snapshot()
    opportunities = service.get_opportunities(min_spread=0.03)

    assert len(snapshot) == 2
    assert len(opportunities) == 1
    assert opportunities[0].buy_source == "polymarket"
