def _check_inconsistent(df: pd.DataFrame, column: str) -> int:
    values = df[column].dropna().astype(str)
    key = values.str.strip().str.lower()
    groups = values.groupby(key).unique()
    bad = {k: list(v) for k, v in groups.items() if len(v) > 1}
    if bad:
        logger.warning("%s has inconsistent values: %s", column, list(bad.values()))
    else:
        logger.info("%s check passed: values are consistent", column)
    return len(bad)

def check_product(df):        return _check_inconsistent(df, "Product")
def check_category(df):       return _check_inconsistent(df, "Category")
def check_payment_method(df): return _check_inconsistent(df, "Payment_Method")
def check_channel(df):        return _check_inconsistent(df, "Channel")
def check_country(df):        return _check_inconsistent(df, "Country")
