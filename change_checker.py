import pandas as pd
from excel_db import read_table
from datetime import datetime, timedelta

def check_recent_changes(ci):
    df = read_table("Change")
    df["start_date"] = pd.to_datetime(df["start_date"])

    last_24h = datetime.now() - timedelta(hours=24)

    return df[
        (df["cmdb_ci"] == ci) &
        (df["start_date"] >= last_24h)
    ]
