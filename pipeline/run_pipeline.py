import logging
import os
from datetime import datetime
from extract import extract_all
from transform import run_transform
from load import load_to_csv

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run():
    logger.info("=== Pipeline started ===")
    raw = extract_all()
    df = run_transform(raw)
    path = load_to_csv(df)
    logger.info(f"=== Pipeline complete. Output: {path} ===")
    return df

if __name__ == '__main__':
    run()