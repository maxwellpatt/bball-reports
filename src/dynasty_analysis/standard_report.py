import pandas as pd
import sqlite3
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.email.email_nba_data import send_email

def get_most_recent_fantrax_data(db_path='data/player_data.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names that start with 'fantrax_'
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'fantrax_%'")
    fantrax_tables = cursor.fetchall()

    if not fantrax_tables:
        print("No Fantrax data found in the database.")
        return None

    # Sort tables by date (assuming format is fantrax_MM_DD_YY)
    def sort_key(table_name):
        _, month, day, year = table_name[0].split('_')
        return int(year), int(month), int(day)

    most_recent_table = sorted(fantrax_tables, key=sort_key, reverse=True)[0][0]

    print(f"Loading most recent Fantrax data: {most_recent_table}")

    # Load the data into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {most_recent_table}", conn)

    conn.close()
    return df

# Load the most recent Fantrax data
fantrax_data = get_most_recent_fantrax_data()


'''
Columns:
Index(['id', 'player', 'team', 'position', 'rkov', 'fantasy_team', 'age',
       'opponent', 'fpts', 'fp_per_g', 'pctd', 'adp', 'fgm', 'fga', '3ptm',
       'ftm', 'fta', 'pts', 'reb', 'ast', 'st', 'blk', 'to', '3d', '2d'],
      dtype='object')
'''

def generate_fpts_distribution(data):
    # Group by fantasy team and calculate mean fantasy points per game
    team_fpts = data.groupby('fantasy_team')['fp_per_g'].mean().sort_values(ascending=False)

    # Create a box plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='fantasy_team', y='fp_per_g', data=data, order=team_fpts.index)
    
    plt.title('Fantasy Points per Game Distribution by Team')
    plt.xlabel('Fantasy Team')
    plt.ylabel('Fantasy Points per Game')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('images/fantasy_points_distribution.png')
    plt.close()

    return team_fpts, 'images/fantasy_points_distribution.png'

team_avg_fpts, image_path = generate_fpts_distribution(fantrax_data)

print("Average Fantasy Points per Game by Team:")
print(team_avg_fpts)

# Prepare email content
email_subject = "Fantasy Points Distribution Report"
email_body = "Please find attached the Fantasy Points per Game Distribution by Team.\n\n"
email_body += "Average Fantasy Points per Game by Team:\n"
email_body += team_avg_fpts.to_string()

# Send email with the image attachment
send_email(email_subject, email_body, attachment_path=image_path)

print("Email sent with the Fantasy Points Distribution image.")
