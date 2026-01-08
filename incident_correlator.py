from excel_db import read_table

def correlate_past_incidents(ci):
    df = read_table("Incident")
    return df[df["cmdb_ci"] == ci]
