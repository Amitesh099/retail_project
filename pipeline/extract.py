import logging
import os

import pandas as pd


logger = logging.getLogger(__name__)

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def extract_train(raw_dir=RAW_DIR):
    path = os.path.join(raw_dir, "train.csv")
    logger.info(f"Extracting train data from {path}")

    df = pd.read_csv(
        path,
        parse_dates=["Date"],
        dtype={"StateHoliday": str},
        low_memory=False,
    )

    logger.info(f"Train data extracted successfully. Shape: {df.shape}")
    return df


def extract_store(raw_dir=RAW_DIR):
    path = os.path.join(raw_dir, "store.csv")
    logger.info(f"Extracting store data from {path}")

    df = pd.read_csv(path)

    logger.info(f"Store data extracted successfully. Shape: {df.shape}")
    return df


def extract_all(raw_dir=RAW_DIR):
    return {
        "train": extract_train(raw_dir),
        "store": extract_store(raw_dir),
    }