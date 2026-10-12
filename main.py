import pandas as pd
from src.load import get_data
from src.validation import (
        check_columns, check_duplicate_order_id, check_quantity,
        check_unit_price, check_discount, check_rating, check_returned,check_order_date
                )
from src.validation import validate
from src.cleaner import clean
from src.analyzer import calculate_kpis,sales_by_product,sales_by_category,sales_by_channel,sales_by_country,sales_by_month
from src.analyzer import generate_outputs, verify_outputs
from src.reporter import generate_charts
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.logger import get_logger

logger = get_logger(__name__)

def run_pipeline():
    logger.info("STEP 1: Loading data")
    df = get_data("data/raw/ecommerce_orders_raw.csv")
    logger.info("STEP 2: First validation")
    validate(df)
    logger.info("STEP 3: Cleaning")
    df = clean(df)
    logger.info("STEP 4: Second validation")
    validate(df)
    logger.info("STEP 5: Generating outputs")
    generate_outputs(df)
    logger.info("STEP 6: Verifying outputs")
    generate_charts(df)
    logger.info("STEP 7: Generate Charts")
    verify_outputs()
    logger.info("PIPELINE COMPLETED")

if __name__ == "__main__":
    #run_pipeline()
    scheduler = BackgroundScheduler()
    scheduler.add_job(
            run_pipeline,
            CronTrigger(hour=6, minute=0),   # every day at 06:00
            id="daily_pipeline",
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600,
                    )
    scheduler.start()
    logger.info("Scheduler started in background")
    try:
        while True:               # keeps the main thread alive
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped")


    
# after check_columns passes:
#check_duplicate_order_id(df)
#check_order_date(df)
#check_quantity(df)
#check_unit_price(df)
#check_discount(df)
#check_rating(df)
#check_returned(df)


#kpis = calculate_kpis(df)
#sbp=sales_by_product(df)
#sbc=sales_by_category(df)
#sbch=sales_by_channel(df)
#sbco=sales_by_country(df)
#sbm=sales_by_month(df)
#print(sbp)
#print(sbc)
#print(sbch)
#print(sbco)
#print(sbm)

    


