import os

# Path to the local cache file
CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache", "prices.json")

# Time-to-live for cached entries in seconds (default: 5 minutes)
CACHE_TTL = 300
