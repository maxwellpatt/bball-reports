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

def perform_kmeans_clustering(data, n_clusters=5):
    """Perform k-means clustering on historical data based on age and FP/G."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['Cluster'] = kmeans.fit_predict(data[['Age', 'FP/G']])
    return kmeans, data

def assign_current_players_to_clusters(kmeans, current_data):
    """Assign current players to the clusters identified in historical data."""
    current_data['Cluster'] = kmeans.predict(current_data[['Age', 'FP/G']])
    return current_data

def plot_clusters(data, title="K-Means Clustering of Players"):
    """Plot the clusters."""
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    
    sns.scatterplot(x='Age', y='FP/G', hue='Cluster', data=data, palette='tab10', legend='full')
    
    plt.title(title)
    plt.xlabel("Age")
    plt.ylabel("Fantasy Points Per Game (FP/G)")
    plt.legend(title='Cluster')
    plt.grid(True)
    plt.show()

def estimate_future_performance(all_time_data, current_data):
    """Estimate future FP/G trajectories for current players based on their clusters."""
    trajectories = []
    
    for cluster in current_data['Cluster'].unique():
        cluster_data = all_time_data[all_time_data['Cluster'] == cluster]
        avg_trajectory = cluster_data.groupby('Age')['FP/G'].mean().reset_index()
        
        for _, player in current_data[current_data['Cluster'] == cluster].iterrows():
            player_trajectory = avg_trajectory.copy()
            player_trajectory['Player'] = player['Player']
            player_trajectory['Current_Age'] = player['Age']
            player_trajectory['Projected_FP/G'] = player_trajectory['FP/G']  # Adjust based on age
            player_trajectory = player_trajectory[player_trajectory['Age'] >= player['Age']]
            trajectories.append(player_trajectory)
    
    return pd.concat(trajectories, ignore_index=True)

if __name__ == "__main__":
    # Step 1: Load the historical and current player data
    all_time_data, current_data = load_data()
    
    # Step 2: Perform k-means clustering on the historical data
    kmeans, all_time_data = perform_kmeans_clustering(all_time_data, n_clusters=5)
    
    # Step 3: Assign current players to the identified clusters
    current_data = assign_current_players_to_clusters(kmeans, current_data)
    
    # Step 4: Plot the clusters for visualization
    plot_clusters(all_time_data, title="K-Means Clustering of Historical Players")
    plot_clusters(current_data, title="Current Players Assigned to Clusters")
    
    # Step 5: Estimate future performance for current players
    future_trajectories = estimate_future_performance(all_time_data, current_data)
    print(future_trajectories.head())

    # Further steps: Analyze and visualize the future trajectories as needed
