import json
import time
from pathlib import Path
from typing import Optional

from config import CACHE_FILE, CACHE_TTL
from models.stock_data import StockData


def _load_cache() -> dict:
    path = Path(CACHE_FILE)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save_cache(cache: dict) -> None:
    path = Path(CACHE_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def get_cached(symbol: str) -> Optional[StockData]:
    """Return a cached StockData entry if it exists and has not expired."""
    cache = _load_cache()
    entry = cache.get(symbol.upper())
    if entry is None:
        return None
    if time.time() - entry.get("timestamp", 0) > CACHE_TTL:
        return None
    stock = StockData.from_dict(entry["data"])
    stock.cached = True
    return stock


def set_cached(stock: StockData) -> None:
    """Persist a StockData entry into the local cache."""
    cache = _load_cache()
    cache[stock.symbol.upper()] = {
        "timestamp": time.time(),
        "data": stock.to_dict(),
    }
    _save_cache(cache)


def clear_cache() -> None:
    """Remove all cached entries."""
    _save_cache({})
