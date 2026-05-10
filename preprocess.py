# preprocess.py
import pandas as pd
import numpy as np
from pathlib import Path
import h5py

# Define constants
DATA_DIR = Path("data")
OUTPUT_DIR = Path("processed")
TARGET_TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h"]
FEATURE_WINDOW_SIZE = 40 * 60  # 40 hours in minutes

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Preprocessing function to generate 40-hour blocks
def preprocess_data(symbol, timeframe):
    input_path = DATA_DIR / f"{symbol}_{timeframe}.parquet"
    output_path = OUTPUT_DIR / f"{symbol}_{timeframe}.h5"

    df = pd.read_parquet(input_path)

    # Generate features
    features = []
    target = []

    for i in range(0, len(df) - FEATURE_WINDOW_SIZE):
        window = df.iloc[i:i+FEATURE_WINDOW_SIZE]
        horizon = df.iloc[i+FEATURE_WINDOW_SIZE:i+FEATURE_WINDOW_SIZE+6]

        window_features = window.iloc[:, 1:].to_numpy().flatten()
        horizon_returns = (horizon['close'] / window['close'].iloc[-1]).to_numpy()

        features.append(window_features)
        target.append(horizon_returns)

    # Save to HDF5
    with h5py.File(output_path, "w") as h5f:
        h5f.create_dataset("features", data=np.array(features), compression="gzip")
        h5f.create_dataset("target", data=np.array(target), compression="gzip")

# Main function to loop over all symbols and timeframes
def main():
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"]  # Extend list

    for symbol in symbols:
        for timeframe in TARGET_TIMEFRAMES:
            preprocess_data(symbol, timeframe)

if __name__ == "__main__":
    main()