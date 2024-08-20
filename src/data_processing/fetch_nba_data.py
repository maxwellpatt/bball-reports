import sqlite3
import os

def fetch_data_for_player(player_name, db_path):
    print(f"Connecting to database at {db_path}...")  # Debugging statement
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player_game_logs';")
    table_exists = cursor.fetchone()
    
    if table_exists is None:
        print("Error: The table 'player_game_logs' does not exist in the database.")
        conn.close()
        return

    print(f"Checking if data for {player_name} exists in the database...")  # Debugging statement
    # Check if data for the player already exists in the database
    cursor.execute("SELECT COUNT(*) FROM player_game_logs WHERE PLAYER_NAME = ?", (player_name,))
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"Data for {player_name} already exists in the database. Skipping fetch.")
    else:
        print(f"Fetching data for {player_name}")  # Debugging statement
        # Add your data fetching and insertion logic here
    
    conn.close()
    print(f"Connection to database closed.")  # Debugging statement

def main():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'player_data.db')
    print(f"Database path: {db_path}")  # Debugging statement

    # List of players to fetch data for
    players = ["Nikola Jokic", "Luka Doncic", "Giannis Antetokounmpo", "Domantas Sabonis", "Anthony Davis"]

    for player in players:
        fetch_data_for_player(player, db_path)

    # Return the filename if needed
    return None  # Adjust this to return the actual file if necessary

if __name__ == "__main__":
    print("Starting the data fetching process...")  # Debugging statement
    main()
    print("Data fetching process completed.")  # Debugging statement
