import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def get_high_fantasy_players(db_path='data/player_data.db', threshold=30):
    """Get players with at least one season of over `threshold` Fantasy Points Per Game."""
    conn = sqlite3.connect(db_path)
    
    query = f"""
    SELECT DISTINCT Player
    FROM all_time_stats
    WHERE [FP/G] > {threshold}
    """
    
    players = pd.read_sql_query(query, conn)
    conn.close()
    
    return players['Player'].tolist()

def get_player_career_stats(player, db_path='data/player_data.db'):
    """Retrieve all seasons of a player's career fantasy stats."""
    conn = sqlite3.connect(db_path)
    
    query = f"""
    SELECT Year, [FP/G]
    FROM all_time_stats
    WHERE Player = ?
    ORDER BY Year
    """
    
    career_stats = pd.read_sql_query(query, conn, params=(player,))
    conn.close()
    
    return career_stats

def plot_all_players_trends(players, db_path='data/player_data.db'):
    """Plot the fantasy points per game trend over all selected players' careers on the same plot."""
    plt.figure(figsize=(12, 8))

    for player in players:
        player_stats = get_player_career_stats(player, db_path)
        if not player_stats.empty:
            plt.plot(player_stats['Year'], player_stats['FP/G'], marker='o', linestyle='-', label=player)
    
    plt.title("Fantasy Points Per Game Trends")
    plt.xlabel("Year")
    plt.ylabel("Fantasy Points Per Game")
    plt.legend(loc="upper left", bbox_to_anchor=(1,1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Step 1: Identify players with at least one season of over 30 FP/G
    players = get_high_fantasy_players()
    
    # Step 2: Plot all players' trends on the same plot
    plot_all_players_trends(players)
