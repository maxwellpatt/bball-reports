import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

import pandas as pd
from src.data_acquisition.download_fantrax_data import main as download_fantrax_data
from src.data.database import db
from src.config.config import config

def load_csv_to_db(file_path, table_name):
    df = pd.read_csv(file_path)
    # Perform any necessary data cleaning or transformations here
    
    # Load data into the database
    db.execute_many(f"""
        INSERT INTO {table_name} ({', '.join(df.columns)})
        VALUES ({', '.join(['?' for _ in df.columns])})
    """, df.values.tolist())

def main():
    # Download the latest Fantrax data
    csv_file_path = download_fantrax_data()
    
    if csv_file_path:
        # Load the downloaded data into the database
        load_csv_to_db(csv_file_path, 'fantrax_data')
        print("Fantrax data successfully updated in the database.")
    else:
        print("Failed to update Fantrax data.")

if __name__ == "__main__":
    main()