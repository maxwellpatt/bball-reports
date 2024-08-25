import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def load_email_config(config_file='config/email_config.yml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def send_email(subject, body, attachment_path=None, config_file='config/email_config.yml'):
    config = load_email_config(config_file)
    
    msg = MIMEMultipart()
    msg['From'] = config['sender_email']
    msg['To'] = config['receiver_email']
    msg['Subject'] = subject
    
    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # Add attachment if provided
    if attachment_path:
        filename = os.path.basename(attachment_path)
        attachment = open(attachment_path, "rb")
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        
        msg.attach(part)
    
    # Use SSL connection
    try:
        server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
        server.login(config['sender_email'], config['password'])
    except smtplib.SMTPException as e:
        # If SSL connection fails, try TLS
        print(f"SSL connection failed: {e}. Trying TLS...")
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['sender_email'], config['password'])
    
    # Send the email
    text = msg.as_string()
    server.sendmail(config['sender_email'], config['receiver_email'], text)
    
    # Quit the server
    server.quit()
    print("Email sent successfully!")

if __name__ == "__main__":

    send_email("Test Subject", "This is a test email.")
