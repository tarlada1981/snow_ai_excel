from excel_db import read_table

def correlate_past_incidents(ci):
    df = read_table("incident")
    return df[df["cmdb_ci"] == ci]
