from excel_db import read_table

def search_kb(problem):
    df = read_table("kb_knowledge")
    return df[df["short_description"].str.contains(problem, case=False)]
