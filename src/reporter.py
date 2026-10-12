# src/reporter.py
from pathlib import Path
import matplotlib 
matplotlib.use("Agg")                      # save images without opening windows
import matplotlib.pyplot as plt
import pandas as pd
from src.logger import get_logger
from src.analyzer import sales_by_month, sales_by_product, sales_by_channel

logger = get_logger(__name__)
REPORTS_DIR = Path("reports")


def _save_figure(fig, filename: str) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / filename
    try:
        fig.tight_layout()
        fig.savefig(path, dpi=150)
    except Exception:
        logger.exception("Could not save chart %s", path)
        raise
    finally:
        plt.close(fig)
        logger.info("Saved chart %s", path)


def chart_sales_by_month(df: pd.DataFrame) -> None:
    data = sales_by_month(df)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data["Month"], data["Total_Sales"], marker="o")
    ax.set_title("Sales by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    _save_figure(fig, "sales_by_month.png")

def chart_sales_by_product(df: pd.DataFrame) -> None:
    data = sales_by_product(df)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(data["Product"], data["Total_Sales"])
    ax.set_title("Sales by Product")
    ax.set_ylabel("Total Sales")
    _save_figure(fig, "sales_by_product.png")

def chart_sales_by_channel(df: pd.DataFrame) -> None:
    data = sales_by_channel(df)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(data["Channel"], data["Total_Sales"])
    ax.set_title("Sales by Channel")
    ax.set_ylabel("Total Sales")
    _save_figure(fig, "sales_by_channel.png")

def generate_charts(df: pd.DataFrame) -> None:
    logger.info("Generating charts")
    chart_sales_by_month(df)
    chart_sales_by_product(df)
    chart_sales_by_channel(df)


