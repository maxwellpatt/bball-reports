import sqlite3
from src.email.email_nba_data import send_email

def fetch_scores_from_db(date='APR 02, 2024'):
    conn = sqlite3.connect('data/player_data.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        MATCHUP,
        SUM(PTS) as total_points,
        WL
    FROM 
        player_game_logs
    WHERE 
        GAME_DATE = ?
    GROUP BY 
        Game_ID, MATCHUP, WL
    ORDER BY 
        MATCHUP;
    '''

    cursor.execute(query, (date,))
    games = cursor.fetchall()
    
    conn.close()

    # Generate a report
    if games:
        report = f"NBA Scores for {date}:\n\n"
        game_dict = {}
        for game in games:
            matchup, total_points, wl = game
            if matchup not in game_dict:
                game_dict[matchup] = {"W": 0, "L": 0}
            game_dict[matchup][wl] = total_points
        
        for matchup, scores in game_dict.items():
            report += f"{matchup}: {scores['W']} - {scores['L']}\n"
    else:
        report = f"No NBA games found for {date}."

    return report

if __name__ == "__main__":
    # Fetch game scores for April 2nd from the database
    scores_report = fetch_scores_from_db(date='APR 02, 2024')
    
    # Send the report via email
    send_email("NBA Game Scores Report for April 2nd", scores_report)
