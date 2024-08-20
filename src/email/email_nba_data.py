import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from data_processing.fetch_nba_data import main as fetch_data
from utils.config import load_email_config

def send_email(filename):
    # Load email configuration
    email_config = load_email_config()

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email_config['sender_email']
    msg['To'] = email_config['receiver_email']
    msg['Subject'] = f"NBA Player Data - {datetime.now().strftime('%Y-%m-%d')}"

    # Email body
    body = "Please find attached the latest NBA player data."
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

def job():
    print("Fetching NBA data...")
    filename = fetch_data()
    if filename:
        send_email(filename)
    else:
        print("No data to send.")

# Schedule the job to run at 1 AM EST
schedule.every().day.at("01:00").do(job)

if __name__ == "__main__":
    print("Scheduler started. Waiting for 1 AM EST to run the job...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute