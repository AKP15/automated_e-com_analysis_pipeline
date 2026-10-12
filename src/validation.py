import pandas as pd
import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)

EXPECTED_COLUMNS = [
        "Order_ID", "Order_Date", "Customer_ID", "Product", "Category",
        "Quantity", "Unit_Price", "Discount", "Sales",
        "Payment_Method", "Channel", "Country", "Rating", "Returned",
                    ]
def check_columns(df: pd.DataFrame) -> bool:
        missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
        extra = [c for c in df.columns if c not in EXPECTED_COLUMNS]
        if extra:
            logger.warning("Unexpected columns found: %s", extra)
        if missing:
            logger.error("Missing columns: %s", missing)
            return False
        logger.info("Column check passed: all %d columns present", len(EXPECTED_COLUMNS))
        return True

def check_duplicate_order_id(df: pd.DataFrame) -> int:
        dupes = df["Order_ID"].duplicated(keep=False).sum()
        if dupes:
            logger.warning("Duplicate Order_ID: %d rows affected", dupes)
        else:
            logger.info("Order_ID check passed: no duplicates")
        return int(dupes)

def check_quantity(df: pd.DataFrame) -> int:
    qty = pd.to_numeric(df["Quantity"], errors="coerce")
    bad = (qty.isna() | (qty <= 0) | (qty % 1 != 0)).sum()
    _report("Quantity", bad)
    return int(bad)

def check_unit_price(df: pd.DataFrame) -> int:
    price = pd.to_numeric(df["Unit_Price"], errors="coerce")
    bad = (price.isna() | (price <= 0)).sum()
    _report("Unit_Price", bad)
    return int(bad)

def check_discount(df: pd.DataFrame) -> int:
    disc = pd.to_numeric(df["Discount"], errors="coerce")
    bad = (disc.isna() | (disc < 0) | (disc > 1)).sum()
    _report("Discount", bad)
    return int(bad)

def check_rating(df: pd.DataFrame) -> int:
    rating = pd.to_numeric(df["Rating"], errors="coerce")
    bad = (rating.isna() | (rating < 1) | (rating > 5)).sum()
    _report("Rating", bad)
    return int(bad)

def check_returned(df: pd.DataFrame) -> int:
    allowed = pd.to_numeric(df["Returned"], errors="coerce")
    bad = (~allowed.isin([0, 1])).sum()
    _report("Returnd", bad)
    return int(bad)

def check_order_date(df: pd.DataFrame) -> int:
    dates = pd.to_datetime(df["Order_Date"], errors="coerce")
    bad = dates.isna().sum()
    _report("Order_Date", bad)
    return int(bad)

def _report(column: str, bad: int) -> None:
    if bad:
        logger.warning("%s check failed: %d invalid rows", column, bad)
    else:
        logger.info("%s check passed", column)

def validate(df: pd.DataFrame) -> bool:
    logger.info("Starting validation")
    if not check_columns(df):
        logger.error("Validation stopped: required columns missing")
        return False
    results = {
            "Order_ID": check_duplicate_order_id(df),
            "Order_Date": check_order_date(df),
            "Quantity": check_quantity(df),
            "Unit_Price": check_unit_price(df),
            "Discount": check_discount(df),
            "Rating": check_rating(df),
            "Returned": check_returned(df),
             }

    total_bad = sum(results.values())
    if total_bad:
        bad_columns = {}
        for k, v in results.items():
            if v > 0:
                bad_columns[k] = v
        logger.warning("Validation finished with issues: %s", bad_columns)
    else:
        logger.info("Validation finished: all checks passed")
    return total_bad == 0

