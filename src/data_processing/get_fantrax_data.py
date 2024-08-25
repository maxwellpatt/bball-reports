import pandas as pd
import sqlite3
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def get_most_recent_fantrax_data(db_path='data/player_data.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names that start with 'fantrax_'
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'fantrax_%'")
    fantrax_tables = cursor.fetchall()

    if not fantrax_tables:
        print("No Fantrax data found in the database.")
        return None

    # Sort tables by date (assuming format is fantrax_MM_DD_YY)
    def sort_key(table_name):
        _, month, day, year = table_name[0].split('_')
        return int(year), int(month), int(day)

    most_recent_table = sorted(fantrax_tables, key=sort_key, reverse=True)[0][0]

    print(f"Loading most recent Fantrax data: {most_recent_table}")

    # Load the data into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {most_recent_table}", conn)

    conn.close()
    return df