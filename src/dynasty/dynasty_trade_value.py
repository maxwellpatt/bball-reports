import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def sigmoid(x, L=1000, k=-0.3, x0=24):
    """Sigmoid function to model potential based on age with a steeper drop-off."""
    return L / (1 + np.exp(-k * (x - x0)))

def exponential_decay(age, decay_rate=0.1):
    """Apply a stronger exponential decay to penalize older players."""
    return np.exp(-decay_rate * (age - 24))  # Penalize more as age increases beyond prime years

def dynamic_weight(age, base_weight=0.5, age_threshold=28):
    """Dynamically adjust the weight of potential vs. performance based on age."""
    if age <= age_threshold:
        return base_weight + (age_threshold - age) * 0.02  # Younger players get more weight on potential
    else:
        return base_weight - (age - age_threshold) * 0.02  # Older players get more weight on performance

def normalize_fp(fp, min_fp, max_fp):
    """Normalize fantasy points per game (FP/G) using min-max scaling."""
    return (fp - min_fp) / (max_fp - min_fp)

def calculate_ceiling(player_name, age, fp, all_time_data, age_tolerance=1, fp_tolerance=5):
    """Calculate the ceiling FP/G based on historical players' career trajectories."""
    if age > 30:
        return fp  # Assume players over 30 have reached their ceiling
    
    similar_players = all_time_data[
        (abs(all_time_data['Age'] - age) <= age_tolerance) &
        (abs(all_time_data['FP/G'] - fp) <= fp_tolerance)
    ]
    
    if not similar_players.empty:
        max_ceiling = similar_players.groupby('Player')['FP/G'].max().max()  # Find the max FP/G peak of similar players
        return max_ceiling
    else:
        return fp  # If no similar players are found, use the current FP/G as a ceiling

def calculate_player_value(age, fp, max_fp, min_fp, ceiling, min_value=100, max_value=1000):
    """Calculate player value based on age, FP/G, and ceiling with dynamic weighting and stronger age penalty."""
    # Exclude players with invalid age or zero FP/G
    if age <= 0 or fp <= 0:
        return min_value  # Assign a minimum value for invalid players
    
    # Calculate potential score using a sigmoid function with exponential decay
    potential_score = sigmoid(age) * exponential_decay(age) * max_value * 0.6  # Stronger age penalty
    
    # Normalize FP/G and scale to 0-1000
    performance_score = normalize_fp(fp, min_fp, max_fp) * max_value
    
    # Calculate ceiling influence with a cap
    ceiling_score = min(ceiling, max_fp) * 0.5  # Reduce influence of the ceiling
    
    # Apply dynamic weight based on age
    weight = dynamic_weight(age)
    
    # Combine the scores with dynamic weights
    player_value = (weight * potential_score) + ((1 - weight) * performance_score) + (0.2 * ceiling_score)
    
    # Ensure the player value is within the desired range
    player_value = np.clip(player_value, min_value, max_value)
    
    return player_value

def load_current_players(db_path='data/player_data.db'):
    """Load current player data from the database."""
    conn = sqlite3.connect(db_path)
    query = "SELECT Player, Age, [FP/G] FROM player_fantasy_stats WHERE [FP/G] > 20"  # Filter players with FP/G > 20
    current_data = pd.read_sql_query(query, conn)
    conn.close()
    return current_data

def load_all_time_data(db_path='data/player_data.db'):
    """Load all-time player data from the database."""
    conn = sqlite3.connect(db_path)
    query = "SELECT Player, Age, [FP/G] FROM all_time_stats WHERE [FP/G] IS NOT NULL"
    all_time_data = pd.read_sql_query(query, conn)
    conn.close()
    return all_time_data

def assign_player_values(players_df, all_time_data):
    """Assign player values to all players in the dataframe."""
    min_fp = players_df['FP/G'].min()
    max_fp = players_df['FP/G'].max()
    
    players_df['Ceiling'] = players_df.apply(
        lambda row: calculate_ceiling(row['Player'], row['Age'], row['FP/G'], all_time_data), axis=1
    )
    
    players_df['Player_Value'] = players_df.apply(
        lambda row: calculate_player_value(row['Age'], row['FP/G'], max_fp, min_fp, row['Ceiling']), axis=1
    )
    
    return players_df

def plot_player_values(players_df):
    """Plot player values to visualize the distribution."""
    plt.figure(figsize=(10, 6))
    plt.hist(players_df['Player_Value'], bins=20, color='blue', edgecolor='black')
    plt.title('Distribution of Player Values')
    plt.xlabel('Player Value')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Load current player data
    current_players = load_current_players()
    
    # Load all-time player data
    all_time_data = load_all_time_data()
    
    # Assign player values based on the scoring model
    valued_players = assign_player_values(current_players, all_time_data)
    
    # Print the top players by value
    top_players = valued_players.sort_values(by='Player_Value', ascending=False)
    print(top_players[['Player', 'Age', 'FP/G', 'Ceiling', 'Player_Value']].head(10))
    
    # Plot the distribution of player values
    plot_player_values(valued_players)
