import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    logger.info("Removed %d duplicate rows", removed)
    return df

def fill_missing_country(df: pd.DataFrame) -> pd.DataFrame:
    country = df["Country"].replace(r"^\s*$", pd.NA, regex=True)
    missing = country.isna().sum()
    df["Country"] = country.fillna("Unknown")
    logger.info("Filled %d missing Country values with 'Unknown'", missing)
    return df

def fill_missing_discount(df: pd.DataFrame) -> pd.DataFrame:
    missing = df["Discount"].isna().sum()
    df["Discount"] = df["Discount"].fillna(0)
    logger.info("Filled %d missing Discount values with 0", missing)
    return df

def flag_negative_price(df: pd.DataFrame) -> pd.DataFrame:
    price = pd.to_numeric(df["Unit_Price"], errors="coerce")
    df["Price_Flag"] = price < 0
    flagged = df["Price_Flag"].sum()
    if flagged:
        logger.warning("Flagged %d rows with negative Unit_Price for investigation", flagged)
    else:
        logger.info("No negative Unit_Price found")
    return df

def standardize_category(df: pd.DataFrame) -> pd.DataFrame:
    changed = (df["Category"] == "electronics").sum()
    df["Category"] = df["Category"].replace({"electronics": "Electronics"})
    logger.info("Standardized %d values in Category", changed)
    return df

def standardize_channel(df: pd.DataFrame) -> pd.DataFrame:
    changed = (df["Channel"] == "website").sum()
    df["Channel"] = df["Channel"].replace({"website": "Website"})
    logger.info("Standardized %d values in Channel", changed)
    return df

def clean(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting cleaning: %d rows", len(df))
    df = df.copy()                 # never change the original data
    df = remove_duplicates(df)
    df = fill_missing_country(df)
    df = fill_missing_discount(df)
    df = standardize_category(df)
    df = standardize_channel(df)
    df = flag_negative_price(df)
    logger.info("Cleaning finished: %d rows", len(df))
    return df
