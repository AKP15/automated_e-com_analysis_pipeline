import pandas as pd
from src.logger import get_logger
from pathlib import Path

logger = get_logger(__name__)

def calculate_kpis(df: pd.DataFrame) -> dict:
    logger.info("Calculating KPIs from %d rows", len(df))
    quantity = pd.to_numeric(df["Quantity"], errors="coerce")
    sales = pd.to_numeric(df["Sales"], errors="coerce")
    returned = pd.to_numeric(df["Returned"], errors="coerce")
    total_orders = df["Order_ID"].nunique()
    total_customers = df["Customer_ID"].nunique()
    total_quantity = int(quantity.sum())
    total_sales = round(float(sales.sum()), 2)
    if total_orders == 0:
        logger.warning("No orders found, AOV set to 0")
        aov = 0.0
    else:
        aov = round(total_sales / total_orders, 2)
        return_rate = round(float(returned.mean()) * 100, 2)
    kpis = {
            "Total Orders": total_orders,
            "Total Customers": total_customers,
            "Total Quantity": total_quantity,
            "Total Sales": total_sales,
            "AOV": aov,
            "Return Rate (%)": return_rate,
            }
    for name, value in kpis.items():
        logger.info(f"KPI | {name} = {value}")
    return kpis

def sales_by_product(df:pd.DataFrame)->pd.DataFrame:
    logger.info("Calculating Sales By Product")
    sales = pd.to_numeric(df["Sales"], errors="coerce")
    sbp=(
            sales.groupby(df["Product"])
            .sum()
            .round(2)
            .sort_values(ascending=False)
            .reset_index(name="Total_Sales")
        )
    if sbp.empty:
        logger.warning("Sales By Product is empty")
        return sbp
    top = sbp.iloc[0]
    logger.info("Top product: %s (%s)", top["Product"], top["Total_Sales"])
    return sbp

def sales_by_category(df:pd.DataFrame)->pd.DataFrame:
    sales = pd.to_numeric(df["Sales"], errors="coerce")
    logger.info("Calculating Sales By Category")
    sbc= (
            sales.groupby(df["Category"])
            .sum()
            .round(2)
            .sort_values(ascending=False)
            .reset_index(name="Total_Sales")
        )
    return sbc

def sales_by_channel(df:pd.DataFrame)->pd.DataFrame:            
    sales = pd.to_numeric(df["Sales"], errors="coerce")         
    logger.info("Calculating Sales By Channel")
    sbch= (
            sales.groupby(df["Channel"])
            .sum()
            .round(2)
            .sort_values(ascending=False)
            .reset_index(name="Total_Sales")
            )                                                   
    return sbch

def sales_by_country(df:pd.DataFrame)->pd.DataFrame:    
    sales = pd.to_numeric(df["Sales"], errors="coerce") 
    logger.info("Calculating Sales By Country")
    sbco= (                                                             
           sales.groupby(df["Country"])
            .sum()
            .round(2)
            .sort_values(ascending=False)               
           .reset_index(name="Total_Sales")                            
           )
    return sbco

def sales_by_month(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Calculating Sales By Month")
    dates = pd.to_datetime(df["Order_Date"], errors="coerce")
    sales = pd.to_numeric(df["Sales"], errors="coerce")
    sbm = (
            sales
            .groupby(dates.dt.to_period("M"))
            .sum()
            .round(2)
            .rename_axis("Month")
            .reset_index(name="Total_Sales")
            )
    sbm["Month"] = sbm["Month"].astype(str)
    return sbm

OUTPUT_DIR = Path("data/outputs")
def save_csv(df: pd.DataFrame, filename: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    try:
        df.to_csv(path, index=False)
    except Exception:
        logger.exception("Could not save %s", path)
        raise
    logger.info("Saved %s (%d rows)", path, len(df))

def generate_outputs(df: pd.DataFrame) -> None:
    logger.info("Generating analysis outputs")
    kpis = calculate_kpis(df)
    kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"])
    save_csv(kpi_df, "kpis.csv")
    tables = {
            "sales_by_product.csv": sales_by_product,
            "sales_by_category.csv": sales_by_category,
            "sales_by_channel.csv": sales_by_channel,
            "sales_by_month.csv": sales_by_month,
                                                }
    for filename, func in tables.items():
        save_csv(func(df), filename)
    logger.info("All outputs saved to %s", OUTPUT_DIR)

EXPECTED_ROWS = {
        "kpis.csv": 6,
        "sales_by_product.csv": 6,
        "sales_by_category.csv": 1,
        "sales_by_channel.csv": 3,
        "sales_by_month.csv": 12,
                            }
def verify_outputs() -> bool:
    logger.info("Verifying output files in %s", OUTPUT_DIR)
    all_ok = True
    for filename, expected in EXPECTED_ROWS.items():
        path = OUTPUT_DIR / filename
        rows = len(pd.read_csv(path)) 
        print(f"{filename:<25}{rows} rows")
        if rows == expected:
            logger.info("OK | %s | %d rows", filename, rows)
        else:
            logger.warning("MISMATCH | %s | %d rows (expected %d)", filename, rows, expected)
            all_ok = False
    return all_ok 
        






                                                
