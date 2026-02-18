from __future__ import annotations

from collections import defaultdict

from app.models import NormalizedMarket, Opportunity


def find_opportunities(markets: list[NormalizedMarket], min_spread: float = 0.03) -> list[Opportunity]:
    grouped: dict[tuple[str, str], list[NormalizedMarket]] = defaultdict(list)
    for market in markets:
        grouped[(market.canonical_id, market.outcome)].append(market)

    opportunities: list[Opportunity] = []
    for (canonical_id, outcome), candidates in grouped.items():
        if len(candidates) < 2:
            continue

        sorted_by_yes = sorted(candidates, key=lambda m: m.yes_price)
        cheapest = sorted_by_yes[0]
        priciest = sorted_by_yes[-1]

        spread = priciest.yes_price - cheapest.yes_price
        if spread < min_spread:
            continue

        liquidity_factor = min(cheapest.liquidity, priciest.liquidity) / 1_000_000
        volume_factor = min(cheapest.volume_24h, priciest.volume_24h) / 1_000_000
        edge_score = spread * (1 + min(liquidity_factor + volume_factor, 2.0))

        opportunities.append(
            Opportunity(
                canonical_id=canonical_id,
                outcome=outcome,
                buy_source=cheapest.source,
                sell_source=priciest.source,
                buy_yes_price=cheapest.yes_price,
                sell_yes_price=priciest.yes_price,
                gross_spread=spread,
                edge_score=round(edge_score, 4),
            )
        )

    return sorted(opportunities, key=lambda o: o.edge_score, reverse=True)
