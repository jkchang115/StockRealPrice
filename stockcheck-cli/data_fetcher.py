import yfinance as yf

from models.stock_data import StockData


def fetch_stock(symbol: str) -> StockData:
    """Fetch real-time stock data from Yahoo Finance for a single ticker."""
    ticker = yf.Ticker(symbol)
    info = ticker.info

    return StockData(
        symbol=symbol.upper(),
        name=info.get("shortName"),
        price=info.get("regularMarketPrice") or info.get("currentPrice"),
        change_pct=info.get("regularMarketChangePercent"),
        volume=info.get("regularMarketVolume"),
        market_cap=info.get("marketCap"),
        sector=info.get("sector"),
        industry=info.get("industry"),
        currency=info.get("currency", "USD"),
    )


def fetch_stocks(symbols: list[str]) -> list[StockData]:
    """Fetch real-time stock data for multiple tickers."""
    return [fetch_stock(sym) for sym in symbols]
