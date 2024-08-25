import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(db_path='data/player_data.db'):
    """Load the all-time stats and current player data from the database."""
    conn = sqlite3.connect(db_path)
    query_all_time = "SELECT Year, Player, Age, [FP/G] FROM all_time_stats WHERE [FP/G] IS NOT NULL"
    query_current = "SELECT Player, Age, [FP/G] FROM player_fantasy_stats WHERE [FP/G] IS NOT NULL"
    
    all_time_data = pd.read_sql_query(query_all_time, conn)
    current_data = pd.read_sql_query(query_current, conn)
    
    conn.close()
    return all_time_data, current_data

def preprocess_data(data):
    """Preprocess the data by removing rows with NaN values."""
    # Drop rows where Age or FP/G is NaN
    data_cleaned = data.dropna(subset=['Age', 'FP/G'])
    return data_cleaned

def perform_kmeans_clustering(data, n_clusters=5):
    """Perform k-means clustering on historical data based on age and FP/G."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['Cluster'] = kmeans.fit_predict(data[['Age', 'FP/G']])
    return kmeans, data

def assign_current_players_to_clusters(kmeans, current_data):
    """Assign current players to the clusters identified in historical data."""
    current_data['Cluster'] = kmeans.predict(current_data[['Age', 'FP/G']])
    return current_data

def amplify_trajectory(trajectory, current_fp, factor=1.5):
    """Amplify the trajectory to make projections more significant."""
    trajectory['Amplified_FP/G'] = trajectory['FP/G'] * (trajectory['FP/G'] / current_fp) ** factor
    return trajectory

def estimate_future_performance(all_time_data, player_name, current_age, current_fp, cluster, years=10):
    """Estimate future FP/G trajectories for a specific player based on their cluster."""
    cluster_data = all_time_data[all_time_data['Cluster'] == cluster]
    avg_trajectory = cluster_data.groupby('Age')['FP/G'].mean().reset_index()
    
    # Amplify the trajectory based on current FP/G
    amplified_trajectory = amplify_trajectory(avg_trajectory, current_fp)
    
    future_projection = []
    for year in range(1, years + 1):
        future_age = current_age + year
        projected_fp = amplified_trajectory[amplified_trajectory['Age'] == future_age]['Amplified_FP/G'].values
        if projected_fp.size > 0:
            future_projection.append((future_age, projected_fp[0]))
        else:
            break  # Stop if we run out of data
    
    return pd.DataFrame(future_projection, columns=['Age', 'Projected_FP/G'])

def plot_projection(player_name, projection):
    """Plot the projected FP/G over the next 10 seasons."""
    plt.figure(figsize=(10, 6))
    plt.plot(projection['Age'], projection['Projected_FP/G'], marker='o', linestyle='-', color='b')
    plt.title(f"Amplified Projected Fantasy Points Per Game for {player_name}")
    plt.xlabel("Age")
    plt.ylabel("Projected Fantasy Points Per Game (FP/G)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Step 1: Load the historical and current player data
    all_time_data, current_data = load_data()
    
    # Step 2: Preprocess the data by removing rows with NaN values
    all_time_data = preprocess_data(all_time_data)
    current_data = preprocess_data(current_data)
    
    # Step 3: Perform k-means clustering on the historical data
    kmeans, all_time_data = perform_kmeans_clustering(all_time_data, n_clusters=5)
    
    # Step 4: Assign current players to the identified clusters
    current_data = assign_current_players_to_clusters(kmeans, current_data)
    
    # Step 5: Focus on Jaylen Brown and Naz Reid
    players_of_interest = ['Jaylen Brown', 'Naz Reid']
    for player in players_of_interest:
        player_data = current_data[current_data['Player'] == player]
        if not player_data.empty:
            cluster = player_data.iloc[0]['Cluster']
            current_age = player_data.iloc[0]['Age']
            current_fp = player_data.iloc[0]['FP/G']
            print(f"Projecting future FP/G for {player}, Age: {current_age}, FP/G: {current_fp}, Cluster: {cluster}")
            
            # Step 6: Estimate future performance for the next 10 seasons
            projection = estimate_future_performance(all_time_data, player, current_age, current_fp, cluster, years=10)
            
            # Step 7: Plot the projection
            plot_projection(player, projection)
        else:
            print(f"No data found for {player}.")
