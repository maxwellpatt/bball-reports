from src.data.database import db
import pandas as pd
from datetime import datetime
import re

def get_most_recent_fantrax_data():
    query = """
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name LIKE 'fantrax_%' AND name NOT LIKE '%trade%'
    """
    tables = db.execute_query(query)

    if not tables:
        print("No Fantrax player data found in the database.")
        return None

    def extract_date(table_name):
        match = re.search(r'(\d{1,2})[_-](\d{1,2})[_-](\d{2,4})', table_name[0])
        if match:
            month, day, year = match.groups()
            year = int(year)
            if year < 100:
                year += 2000
            return datetime(year, int(month), int(day))
        return datetime(1900, 1, 1)

    most_recent_table = sorted(tables, key=extract_date, reverse=True)[0][0]
    print(f"Loading most recent Fantrax data: {most_recent_table}")

    query = f"SELECT * FROM {most_recent_table}"
    df = pd.DataFrame(db.execute_query(query))
    
    print(f"Columns in the DataFrame: {df.columns.tolist()}")
    return df