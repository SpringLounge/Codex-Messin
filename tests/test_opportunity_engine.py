from datetime import datetime, timedelta, timezone

from app.models import NormalizedMarket
from app.opportunity_engine import find_opportunities


def _market(source: str, yes_price: float, canonical: str = "event_a") -> NormalizedMarket:
    return NormalizedMarket(
        source=source,
        market_id=f"{source}-{canonical}",
        title="Test",
        canonical_id=canonical,
        outcome="YES",
        yes_price=yes_price,
        no_price=1 - yes_price,
        volume_24h=1_000_000,
        liquidity=1_000_000,
        close_time=datetime.now(timezone.utc) + timedelta(days=1),
    )


def test_find_opportunities_detects_spread():
    markets = [_market("polymarket", 0.40), _market("kalshi", 0.48)]
    opportunities = find_opportunities(markets, min_spread=0.03)

    assert len(opportunities) == 1
    top = opportunities[0]
    assert top.buy_source == "polymarket"
    assert top.sell_source == "kalshi"
    assert round(top.gross_spread, 2) == 0.08


def test_find_opportunities_respects_threshold():
    markets = [_market("polymarket", 0.40), _market("kalshi", 0.42)]
    opportunities = find_opportunities(markets, min_spread=0.03)

    assert opportunities == []
