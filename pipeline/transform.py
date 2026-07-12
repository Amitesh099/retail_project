import logging

import pandas as pd


logger = logging.getLogger(__name__)


def clean_store(store: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning store data...")

    df = store.copy()

    df["CompetitionDistance"] = df["CompetitionDistance"].fillna(
        df["CompetitionDistance"].median()
    )
    df["CompetitionOpenSinceMonth"] = df["CompetitionOpenSinceMonth"].fillna(0)
    df["CompetitionOpenSinceYear"] = df["CompetitionOpenSinceYear"].fillna(0)
    df["Promo2SinceWeek"] = df["Promo2SinceWeek"].fillna(0)
    df["Promo2SinceYear"] = df["Promo2SinceYear"].fillna(0)
    df["PromoInterval"] = df["PromoInterval"].fillna("None")

    logger.info(f"Store data cleaned. Remaining null values: {df.isnull().sum().sum()}")
    return df


def clean_train(train: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning train data...")

    df = train.copy()

    df["StateHoliday"] = df["StateHoliday"].astype(str).replace("0", "none")

    # Stores marked open but having zero sales are treated as anomalous/closed days.
    df.loc[(df["Open"] == 1) & (df["Sales"] == 0), "Open"] = 0

    # Closed days are not useful for store-level sales forecasting.
    df = df[df["Open"] == 1].copy()

    logger.info(f"Train data cleaned. Open-store rows retained: {len(df)}")
    return df


def merge_datasets(train: pd.DataFrame, store: pd.DataFrame) -> pd.DataFrame:
    logger.info("Merging train and store datasets...")

    df = train.merge(store, on="Store", how="left")

    logger.info(f"Merged dataset shape: {df.shape}")
    logger.info(f"Remaining null values after merge: {df.isnull().sum().sum()}")

    return df


def run_transform(raw_data: dict) -> pd.DataFrame:
    store_clean = clean_store(raw_data["store"])
    train_clean = clean_train(raw_data["train"])
    merged_df = merge_datasets(train_clean, store_clean)

    return merged_df