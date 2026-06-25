import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def clean_store(store: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning store data...")
    df = store.copy()
    df['CompetitionDistance'] = df['CompetitionDistance'].fillna(
        df['CompetitionDistance'].median())
    df['CompetitionOpenSinceMonth'] = df['CompetitionOpenSinceMonth'].fillna(0)
    df['CompetitionOpenSinceYear'] = df['CompetitionOpenSinceYear'].fillna(0)
    df['Promo2SinceWeek'] = df['Promo2SinceWeek'].fillna(0)
    df['Promo2SinceYear'] = df['Promo2SinceYear'].fillna(0)
    df['PromoInterval'] = df['PromoInterval'].fillna('None')
    logger.info(f"Store cleaned. Nulls remaining: {df.isnull().sum().sum()}")
    return df

def clean_train(train: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning train data...")
    df = train.copy()
    df['StateHoliday'] = df['StateHoliday'].astype(str).replace('0', 'none')
    df.loc[(df['Open'] == 1) & (df['Sales'] == 0), 'Open'] = 0
    df = df[df['Open'] == 1].copy()
    logger.info(f"Train cleaned. Open days only: {len(df)}")
    return df

def merge_datasets(train: pd.DataFrame, store: pd.DataFrame) -> pd.DataFrame:
    logger.info("Merging train and store...")
    df = train.merge(store, on='Store', how='left')
    logger.info(f"Merged shape: {df.shape}, Nulls: {df.isnull().sum().sum()}")
    return df

def run_transform(raw_data: dict) -> pd.DataFrame:
    store_clean = clean_store(raw_data['store'])
    train_clean = clean_train(raw_data['train'])
    df = merge_datasets(train_clean, store_clean)
    return df