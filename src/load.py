import pandas as pd
from src.logger import get_logger
from pathlib import Path

logger = get_logger(__name__)
def get_data(data_path: str) -> pd.DataFrame:
    path= data_path
    if path is None:
        logger.error("No data path provided.")
        raise ValueError("No data path provided.")

    logger.info("Loading data from %s", data_path)       
    return pd.read_csv(path)
    logger.info("Loaded %d rows and %d columns", df.shape[0], df.shape[1])
    return df



def save_data(df: pd.DataFrame, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_csv(path, index=False)
    except Exception:
        logger.exception("Could not save data to %s", path)
        raise
    logger.info("Saved %d rows and %d columns to %s", df.shape[0], df.shape[1], path)
