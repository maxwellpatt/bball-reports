import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_all_time_data(db_path='data/player_data.db'):
    """Load the all-time stats data from the database."""
    conn = sqlite3.connect(db_path)
    query = "SELECT Year, Player, Age, [FP/G] FROM all_time_stats WHERE [FP/G] IS NOT NULL"
    all_time_data = pd.read_sql_query(query, conn)
    conn.close()
    return all_time_data

def stratify_data(data, fp_bins, age_bins):
    """Stratify the data by fantasy points per game and age."""
    data['FP/G_bin'] = pd.cut(data['FP/G'], bins=fp_bins, include_lowest=True)
    data['Age_bin'] = pd.cut(data['Age'], bins=age_bins, include_lowest=True)
    return data

def calculate_aging_curves(stratified_data):
    """Calculate the average FP/G at each age for each stratum."""
    aging_curves = stratified_data.groupby(['FP/G_bin', 'Age_bin', 'Age'])['FP/G'].mean().reset_index()
    return aging_curves

def plot_aging_curves(aging_curves):
    """Plot the aging curves for each stratum."""
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))

    for (fp_bin, age_bin), group in aging_curves.groupby(['FP/G_bin', 'Age_bin']):
        plt.plot(group['Age'], group['FP/G'], marker='o', label=f'FP/G: {fp_bin}, Age: {age_bin}')

    plt.title("Aging Curves Stratified by FP/G and Age")
    plt.xlabel("Age")
    plt.ylabel("Fantasy Points Per Game (FP/G)")
    plt.legend(loc="upper right", bbox_to_anchor=(1.15, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Step 1: Load the historical data
    all_time_data = load_all_time_data()
    
    # Step 2: Stratify the data by FP/G and age
    fp_bins = [0, 10, 20, 30, 40, 50]  # Example FP/G bins
    age_bins = [18, 24, 28, 32, 36, 40]  # Example age bins
    stratified_data = stratify_data(all_time_data, fp_bins, age_bins)
    
    # Step 3: Calculate aging curves
    aging_curves = calculate_aging_curves(stratified_data)
    
    # Step 4: Plot aging curves
    plot_aging_curves(aging_curves)
