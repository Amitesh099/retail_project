import os
import logging

logger = logging.getLogger(__name__)

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

def load_to_csv(df, filename='rossmann_cleaned.csv', out_dir=PROCESSED_DIR):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    df.to_csv(path, index=False)
    logger.info(f"Saved {len(df)} rows to {path}")
    return path