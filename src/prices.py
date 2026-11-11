from pathlib import Path

import yfinance as yf

from config import TICKERS

DATA_DIR = Path("data/prices")

# (label, how far back, bar size)
DOWNLOADS = [
    ("daily", "6mo", "1d"),
    ("hourly", "1mo", "1h"),
]


def download_prices(symbol, period, interval):
    """Download OHLCV bars for one stock, with timestamps in UTC."""
    df = yf.Ticker(symbol).history(period=period, interval=interval)
    if df.empty:
        return df
    df.index = df.index.tz_convert("UTC")
    df.index.name = "timestamp_utc"
    return df[["Open", "High", "Low", "Close", "Volume"]]


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for exchange, stocks in TICKERS.items():
        for symbol, name in stocks.items():
            for label, period, interval in DOWNLOADS:
                df = download_prices(symbol, period, interval)
                if df.empty:
                    print(f"[{exchange}] {name} ({symbol}) {label}: NO DATA")
                    continue
                path = DATA_DIR / f"{symbol}_{label}.csv"
                df.to_csv(path)
                print(f"[{exchange}] {name} ({symbol}) {label}: {len(df)} rows -> {path}")


if __name__ == "__main__":
    main()