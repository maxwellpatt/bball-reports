import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.email.email_nba_data import send_email
from src.data_processing.get_fantrax_data import get_most_recent_fantrax_data
from src.config.config import config

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
