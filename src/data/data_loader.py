import csv
from pathlib import Path
from typing import List, Dict, Any

def load_csv_data(file_path: str) -> List[Dict[str, Any]]:
    data_path = Path(__file__).parent.parent.parent / 'data' / file_path
    with open(data_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def get_league_data() -> List[Dict[str, Any]]:
    return load_csv_data('fantrax_8_9_24.csv')