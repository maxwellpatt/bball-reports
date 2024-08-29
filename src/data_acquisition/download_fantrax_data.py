import os
import time
import pandas as pd
from src.data_acquisition.fantrax_api import FantraxAPIWrapper

def download_fantrax_data(output_dir):
    api_wrapper = FantraxAPIWrapper()
    
    try:
        players = api_wrapper.get_players()
        if players:
            filename = f"fantrax_data_{time.strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(output_dir, filename)
            
            df = pd.DataFrame(players)
            df.to_csv(filepath, index=False)
            
            print(f"Data downloaded and saved to {filepath}")
            return filepath
        else:
            print("Failed to retrieve player data")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        api_wrapper.logout()

def main():
    output_dir = "data/raw/fantrax"
    os.makedirs(output_dir, exist_ok=True)
    return download_fantrax_data(output_dir)

if __name__ == "__main__":
    main()