# config.py
from pathlib import Path

# Central configuration for the cryptocurrency forecasting system

# File paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHECKPOINT_DIR = BASE_DIR / "checkpoints"
MAPPING_FILE = BASE_DIR / "mapping.json"

# Cryptocurrency pairs to process (examples, extend to 500 pairs in practice)
CRYPTO_PAIRS = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT"
    # Add up to 500 pairs
]

# Target timeframes
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h"]

# Data preprocessing
FEATURE_WINDOW = 40  # in hours

# Group settings
GROUP_SIZE = 50  # Number of tokens per group

# Training hyperparameters
BATCH_SIZE = 1    # Single sample per batch
LEARNING_RATE = 1e-4
EPOCHS = 100
DELTA = 0.5       # Huber loss delta
SAVE_EVERY = 1000 # Checkpoint every N blocks

# Mixed precision
USE_MIXED_PRECISION = True