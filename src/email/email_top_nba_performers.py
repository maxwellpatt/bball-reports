import sqlite3
import random
import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.email.email_nba_data import send_email

def fetch_top_fantasy_performers(date):
    conn = sqlite3.connect('data/player_data.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        PLAYER_NAME,
        GAME_DATE,
        (AST * 2) + 
        (BLK * 4) + 
        (FGA * -1) + 
        (FGM * 2) + 
        (FTA * -1) + 
        (FTM * 1) + 
        (PTS * 1) + 
        (REB * 1) + 
        (STL * 4) + 
        (FG3M * 1) + 
        (IFNULL('3D', 0) * 3) + 
        (IFNULL('2D', 0) * 2) + 
        (TOV * -2) AS fantasy_score
    FROM 
        player_game_logs
    WHERE 
        GAME_DATE = ?
    ORDER BY 
        fantasy_score DESC
    LIMIT 25;
    '''

    cursor.execute(query, (date,))
    top_players = cursor.fetchall()
    
    conn.close()

    return top_players

def generate_report(players, date):
    report = f"Top 25 Fantasy Performances for {date}:\n\n"
    for player in players:
        report += f"Player: {player[0]}, Fantasy Score: {player[2]:.2f}\n"
    return report

if __name__ == "__main__":
    # Randomly select a date from your dataset
    date = random.choice([
        "APR 02, 2024",
        "APR 03, 2024",
        "APR 04, 2024",
        # Add more dates as needed
    ])
    
    # Fetch top 25 players
    top_players = fetch_top_fantasy_performers(date)
    
    # Generate the report
    report = generate_report(top_players, date)
    
    # Send the email with the report
    send_email(f"Top 25 Fantasy Performances for {date}", report)
