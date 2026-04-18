#!/usr/bin/env python3
"""stockcheck – CLI entry point."""

import json
import sys

import config as cfg
from cache_manager import clear_cache, get_cached, set_cached
from cli.parser import build_parser
from data_fetcher import fetch_stock, fetch_stocks
from sector_mapper import group_by_sector, sector_label


# ──────────────────────────────────────────────
# Formatting helpers
# ──────────────────────────────────────────────

def _fmt_price(price, currency):
    if price is None:
        return "N/A"
    sym = "$" if currency == "USD" else (currency or "")
    return f"{sym}{price:,.2f}"


def _fmt_change(change_pct):
    if change_pct is None:
        return "  N/A  "
    sign = "+" if change_pct >= 0 else ""
    return f"{sign}{change_pct:.2f}%"


def _fmt_volume(volume):
    if volume is None:
        return "N/A"
    if volume >= 1_000_000:
        return f"{volume / 1_000_000:.1f}M"
    if volume >= 1_000:
        return f"{volume / 1_000:.1f}K"
    return str(volume)


def _fmt_market_cap(market_cap):
    if market_cap is None:
        return "N/A"
    if market_cap >= 1_000_000_000_000:
        return f"${market_cap / 1_000_000_000_000:.2f}T"
    if market_cap >= 1_000_000_000:
        return f"${market_cap / 1_000_000_000:.2f}B"
    if market_cap >= 1_000_000:
        return f"${market_cap / 1_000_000:.2f}M"
    return f"${market_cap:,}"


def _print_header():
    print(
        f"{'Symbol':<8} {'Name':<28} {'Price':>12} {'Change':>9} "
        f"{'Volume':>8} {'Mkt Cap':>12} {'Sector':<16} {'Industry'}"
    )
    print("-" * 120)


def _print_stock(stock):
    cached_tag = " [cache]" if stock.cached else ""
    print(
        f"{stock.symbol:<8} {(stock.name or 'N/A'):<28} "
        f"{_fmt_price(stock.price, stock.currency):>12} "
        f"{_fmt_change(stock.change_pct):>9} "
        f"{_fmt_volume(stock.volume):>8} "
        f"{_fmt_market_cap(stock.market_cap):>12} "
        f"{sector_label(stock.sector):<16} "
        f"{stock.industry or 'N/A'}"
        f"{cached_tag}"
    )


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    parser = build_parser()
    args = parser.parse_args()

    # --clear-cache: wipe cache and exit
    if args.clear_cache:
        clear_cache()
        print("Cache cleared.")
        sys.exit(0)

    # Override TTL if requested
    if args.ttl is not None:
        cfg.CACHE_TTL = args.ttl

    results = []
    symbols = [s.upper() for s in args.symbols]

    to_fetch: list[str] = []
    cached_results: dict[str, object] = {}

    # Check cache for each symbol first
    for symbol in symbols:
        if not args.no_cache:
            cached = get_cached(symbol)
            if cached is not None:
                cached_results[symbol] = cached
                continue
        to_fetch.append(symbol)

    # Batch-fetch all cache-miss symbols
    if to_fetch:
        try:
            fresh = fetch_stocks(to_fetch)
        except Exception as exc:
            print(f"ERROR: Could not fetch data: {exc}", file=sys.stderr)
            fresh = []

        for stock in fresh:
            set_cached(stock)
            cached_results[stock.symbol] = stock

    # Assemble results in original symbol order
    for symbol in symbols:
        stock = cached_results.get(symbol)
        if stock is None:
            print(f"ERROR: No data available for {symbol}.", file=sys.stderr)
        else:
            results.append(stock)

    if not results:
        sys.exit(1)

    # ── JSON output ──────────────────────────────
    if args.output_json:
        output = [s.to_dict() for s in results]
        print(json.dumps(output, indent=2))
        return

    # ── Grouped output ───────────────────────────
    if args.group_by_sector:
        groups = group_by_sector(results)
        for sector, stocks in groups.items():
            print(f"\n── {sector} ──")
            _print_header()
            for s in stocks:
                _print_stock(s)
        return

    # ── Default tabular output ───────────────────
    _print_header()
    for s in results:
        _print_stock(s)


if __name__ == "__main__":
    main()
