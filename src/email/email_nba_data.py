import sys
import os

# Add the `src` directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Now import the config module
from utils.config import load_email_config
import sqlite3  # Import sqlite3 for database operations
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

# Step 1: Fetch Data from the player_fantasy_stats Table
def fetch_fantasy_stats():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'player_data.db'))
    print(f"Using database at: {db_path}")  # Print the absolute path for verification
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM player_fantasy_stats"
    fantasy_stats_df = pd.read_sql_query(query, conn)
    conn.close()
    return fantasy_stats_df


# Step 2: Save Data to CSV
def save_to_csv(df, filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    df.to_csv(filepath, index=False)
    return filepath

def send_email(filename):
    # Load email configuration
    email_config = load_email_config()

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email_config['sender_email']
    msg['To'] = email_config['receiver_email']
    msg['Subject'] = f"NBA Player Fantasy Stats - {datetime.now().strftime('%Y-%m-%d')}"

    # Email body
    body = "Please find attached the latest NBA player fantasy stats."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the CSV file
    with open(filename, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(filename))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
    msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP_SSL(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.login(email_config['sender_email'], email_config['sender_password'])
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def main():
    # Fetch data from the player_fantasy_stats table
    fantasy_stats_df = fetch_fantasy_stats()

    # Save the DataFrame to a CSV file
    csv_filename = "fantasy_stats.csv"
    csv_filepath = save_to_csv(fantasy_stats_df, csv_filename)

    # Send the CSV file via email
    send_email(csv_filepath)

if __name__ == "__main__":
    main()
