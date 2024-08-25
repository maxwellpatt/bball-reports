import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def career_trajectory_by_age(age, peak_age=28, max_fp=70):
    """
    Calculate the career trajectory based on the player's current age.
    The trajectory peaks at peak_age and declines afterward.
    """
    if age < peak_age:
        # Rising curve for younger players
        years_to_peak = peak_age - age
        trajectory = np.linspace(1, max_fp, years_to_peak)
        decline = np.linspace(max_fp, 1, 36 - peak_age)
        full_trajectory = np.concatenate((trajectory, decline))
    else:
        # Declining curve for older players
        years_past_peak = age - peak_age
        rise = np.linspace(1, max_fp, peak_age - 20)
        trajectory = np.linspace(max_fp, 1, 36 - peak_age)
        full_trajectory = np.concatenate((rise[years_past_peak:], trajectory))

    return full_trajectory[:36 - age]

def plot_trajectory(player_name, age):
    """Plot the career trajectory for a given player based on their current age."""
    trajectory = career_trajectory_by_age(age)
    plt.plot(np.arange(age, age + len(trajectory)), trajectory, label=f"{player_name} at age {age}")

def load_current_players(db_path='data/player_data.db'):
    """Load current player data from the database."""
    conn = sqlite3.connect(db_path)
    query = "SELECT Player, Age, [FP/G] FROM player_fantasy_stats WHERE [FP/G] > 20"  # Filter players with FP/G > 20
    current_data = pd.read_sql_query(query, conn)
    conn.close()
    return current_data

if __name__ == "__main__":
    # Load current player data
    current_players = load_current_players()
    
    # Filter for the specific players: Jaylen Brown, Victor Wembanyama, Pascal Siakam
    target_players = current_players[current_players['Player'].isin(['Jaylen Brown', 'Victor Wembanyama', 'Pascal Siakam'])]
    
    # Plot the trajectory for each of the target players
    for index, row in target_players.iterrows():
        plot_trajectory(row['Player'], row['Age'])
    
    # Finalize and show the plot
    plt.xlabel("Age")
    plt.ylabel("Fantasy Points Per Game (FP/G)")
    plt.title("Career Trajectories of Selected Players")
    plt.legend()
    plt.show()
