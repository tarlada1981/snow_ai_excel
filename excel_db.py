import pandas as pd

EXCEL_FILE = "snow_dummy_data.xlsx"

def read_table(sheet):
    return pd.read_excel(EXCEL_FILE, sheet_name=sheet)
