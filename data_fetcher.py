
import yfinance as yf
import pandas as pd

class DataFetcher:

    def get_price(self, ticker: str):

        try:
            data = yf.Ticker(ticker)

            info = data.info

            return {
                "ticker": ticker,
                "price": info.get("currentPrice"),
                "sector": info.get("sector"),
                "marketCap": info.get("marketCap")
            }

        except Exception as e:

            print(f"API error: {ticker}")

            return None