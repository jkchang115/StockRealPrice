# stockcheck-cli

A command-line tool that fetches real-time stock prices from **Yahoo Finance** with local TTL-based caching, sector/industry grouping, and flexible output formats.

---

## Project Structure

```
stockcheck-cli/
│
├─ stockcheck.py          # CLI entry point
│
├─ data_fetcher.py        # Yahoo Finance API (yfinance)
├─ cache_manager.py       # Local TTL cache (JSON-backed)
├─ sector_mapper.py       # Sector / industry helpers
│
├─ cli/
│   └─ parser.py          # argparse CLI definition
│
├─ models/
│   └─ stock_data.py      # StockData dataclass
│
├─ config.py              # Configuration constants
├─ requirements.txt       # Python dependencies
│
├─ cache/
│   └─ prices.json        # Local cache file
│
└─ README.md
```

---

## Installation

```bash
cd stockcheck-cli
pip install -r requirements.txt
```

---

## Usage

```
python stockcheck.py [OPTIONS] SYMBOL [SYMBOL ...]
```

### Positional arguments

| Argument  | Description                                          |
|-----------|------------------------------------------------------|
| `SYMBOL`  | One or more ticker symbols (e.g. `AAPL MSFT TSLA`)  |

### Options

| Flag                | Description                                               |
|---------------------|-----------------------------------------------------------|
| `--no-cache`        | Bypass local cache and always fetch fresh data            |
| `--clear-cache`     | Clear all cached entries and exit                         |
| `--group-by-sector` | Group output by sector                                    |
| `--ttl SECONDS`     | Override the default cache TTL (default: 300 s)           |
| `--json`            | Output results as JSON                                    |

---

## Examples

```bash
# Fetch prices for Apple and Microsoft
python stockcheck.py AAPL MSFT

# Skip the cache
python stockcheck.py AAPL --no-cache

# Group multiple tickers by sector
python stockcheck.py AAPL MSFT AMZN GOOGL TSLA JPM XOM --group-by-sector

# Output as JSON
python stockcheck.py AAPL TSLA --json

# Set a custom TTL of 60 seconds
python stockcheck.py AAPL --ttl 60

# Clear the local cache
python stockcheck.py --clear-cache AAPL
```

---

## Configuration

Edit **`config.py`** to change defaults:

| Variable       | Default                    | Description                        |
|----------------|----------------------------|------------------------------------|
| `CACHE_FILE`   | `cache/prices.json`        | Path to the JSON cache file        |
| `CACHE_TTL`    | `300`                      | Cache time-to-live in seconds      |
| `YAHOO_FIELDS` | *(list)*                   | Yahoo Finance fields to retrieve   |

---

## How It Works

1. **CLI parsing** (`cli/parser.py`) validates user arguments via `argparse`.
2. **Cache lookup** (`cache_manager.py`) checks `cache/prices.json` for a non-expired entry.
3. **Data fetch** (`data_fetcher.py`) queries Yahoo Finance via `yfinance` on cache miss.
4. **Sector mapping** (`sector_mapper.py`) provides labels and grouping logic.
5. **Output** is rendered as a formatted table, sector-grouped table, or JSON.
