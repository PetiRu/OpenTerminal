# downloader.py
import ccxt
import pandas as pd
from datetime import datetime
from pathlib import Path
import time

# Define constants
DATA_DIR = Path("data")
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h"]
START_DATE = "2020-01-01T00:00:00Z"
LIMIT = 1000  # Max candles per API call

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Binance exchange
exchange = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True
})

# Function to download OHLCV data for a pair and timeframe
def download_ohlcv(pair, timeframe):
    print(f"Downloading {pair} {timeframe} data...")
    
    since = exchange.parse8601(START_DATE)
    all_data = []

    while True:
        try:
            ohlcv = exchange.fetch_ohlcv(pair, timeframe, since, LIMIT)
            if not ohlcv:
                break
            
            since = ohlcv[-1][0] + 1  # Move to the next batch
            all_data.extend(ohlcv)

            # Respect rate limits
            time.sleep(exchange.rateLimit / 1000)

        except Exception as e:
            print(f"Error fetching data: {e}")
            break

    # Convert to DataFrame
    df = pd.DataFrame(all_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Save to Parquet
    save_path = DATA_DIR / f"{pair.replace('/', '_')}_{timeframe}.parquet"
    df.to_parquet(save_path, index=False)
    print(f"Saved {pair} {timeframe} data to {save_path}")

# Main function to iterate over all pairs and timeframes
def main():
    pairs = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT"
        # Extend to 500 pairs
    ]

    for pair in pairs:
        for timeframe in TIMEFRAMES:
            download_ohlcv(pair, timeframe)

if __name__ == "__main__":
    main()