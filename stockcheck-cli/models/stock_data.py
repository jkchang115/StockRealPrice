from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StockData:
    symbol: str
    name: Optional[str] = None
    price: Optional[float] = None
    change_pct: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[int] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    currency: Optional[str] = "USD"
    cached: bool = False

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "price": self.price,
            "change_pct": self.change_pct,
            "volume": self.volume,
            "market_cap": self.market_cap,
            "sector": self.sector,
            "industry": self.industry,
            "currency": self.currency,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StockData":
        return cls(
            symbol=data.get("symbol", ""),
            name=data.get("name"),
            price=data.get("price"),
            change_pct=data.get("change_pct"),
            volume=data.get("volume"),
            market_cap=data.get("market_cap"),
            sector=data.get("sector"),
            industry=data.get("industry"),
            currency=data.get("currency", "USD"),
        )
