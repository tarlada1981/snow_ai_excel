import pandas as pd

EXCEL_FILE = "SNOWDummy_fill.xlsx"

def read_table(sheet):
    return pd.read_excel(EXCEL_FILE, sheet_name=sheet)
