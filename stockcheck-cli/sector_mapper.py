"""
Lightweight sector/industry helper.

Provides human-readable labels and simple grouping utilities on top of the
sector and industry strings already returned by Yahoo Finance.
"""

# Canonical sector ordering used when sorting output
SECTOR_ORDER = [
    "Technology",
    "Communication Services",
    "Consumer Cyclical",
    "Consumer Defensive",
    "Energy",
    "Financial Services",
    "Healthcare",
    "Industrials",
    "Basic Materials",
    "Real Estate",
    "Utilities",
]

# Short aliases / display labels
SECTOR_LABELS: dict[str, str] = {
    "Technology": "Tech",
    "Communication Services": "Comm",
    "Consumer Cyclical": "Cons-Cyc",
    "Consumer Defensive": "Cons-Def",
    "Energy": "Energy",
    "Financial Services": "Finance",
    "Healthcare": "Health",
    "Industrials": "Ind",
    "Basic Materials": "Materials",
    "Real Estate": "RE",
    "Utilities": "Util",
}


def sector_label(sector: str | None) -> str:
    """Return a short display label for *sector*, or 'N/A' if unknown."""
    if sector is None:
        return "N/A"
    return SECTOR_LABELS.get(sector, sector)


def group_by_sector(stocks: list) -> dict[str, list]:
    """
    Group a list of StockData objects by sector.

    Returns an ordered dict keyed by sector name; stocks with no sector are
    placed under the key ``'Other'``.
    """
    groups: dict[str, list] = {}
    for stock in stocks:
        key = stock.sector or "Other"
        groups.setdefault(key, []).append(stock)

    # Sort groups by canonical sector order; unknown sectors go last
    def _order(sector: str) -> int:
        try:
            return SECTOR_ORDER.index(sector)
        except ValueError:
            return len(SECTOR_ORDER)

    return dict(sorted(groups.items(), key=lambda kv: _order(kv[0])))
