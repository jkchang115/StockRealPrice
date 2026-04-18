import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stockcheck",
        description="Fetch real-time stock prices from Yahoo Finance with local TTL caching.",
    )

    parser.add_argument(
        "symbols",
        nargs="+",
        metavar="SYMBOL",
        help="One or more stock ticker symbols (e.g. AAPL MSFT TSLA).",
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        default=False,
        help="Bypass the local cache and always fetch fresh data.",
    )

    parser.add_argument(
        "--clear-cache",
        action="store_true",
        default=False,
        help="Clear all locally cached entries and exit.",
    )

    parser.add_argument(
        "--group-by-sector",
        action="store_true",
        default=False,
        help="Group output by sector.",
    )

    parser.add_argument(
        "--ttl",
        type=int,
        default=None,
        metavar="SECONDS",
        help="Override the default cache TTL (seconds).",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        dest="output_json",
        help="Output results as JSON.",
    )

    return parser
