import smtplib
import os
from email.message import EmailMessage
from cryptography.fernet import Fernet
import logging
from datetime import datetime

# Configuration for email
smtp_port = 587

# Config groups for loop
folder_configs = [
    {
        "source_folder": "/home/user/Desktop/pyproject/test/email",  # Update with the correct path
        "archive_folder": "/home/user/Desktop/pyproject/test/archive",  # Update with the correct path
        "to_emails": ["group1@example.com"],
        "subject": "Group 1: OPERA SSP H&F Reports",
        "body": """<html>
                    <body>
                        <p>Group 1: OPERA SSP H&F TR and RR Reports Attached</p>
                        <p>Additional Information:</p>
                        <ul>
                            <li>Report 1: Details...</li>
                            <li>Report 2: Details...</li>
                            <li>Report 3: Details...</li>
                        </ul>
                    </body>
                   </html>"""
    },
    {
        "source_folder": "/home/user/Desktop/pyproject/test/email",  # Update with the correct path
        "archive_folder": "/home/user/Desktop/pyproject/test/archive",  # Update with the correct path
        "to_emails": ["group2@example.com"],
        "subject": "Group 2: OPERA SSP H&F Reports",
        "body": """<html>
                    <body>
                        <p>Group 2: OPERA SSP H&F TR and RR Reports Attached</p>
                        <p>Additional Information:</p>
                        <ul>
                            <li>Report 1: Details...</li>
                            <li>Report 2: Details...</li>
                            <li>Report 3: Details...</li>
                        </ul>
                    </body>
                   </html>"""
    }
]

# Define the log folder and log file name
log_folder = "/path/to/logFolder"  # Update with the correct path
log_file = os.path.join(log_folder, f"email_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load the key
with open('key.key', 'rb') as key_file:
    key = key_file.read()

# Initialize the Fernet object with the key
cipher_suite = Fernet(key)

# Decrypt the email, SMTP server, and password
with open('encrypted_from_email.bin', 'rb') as file:
    encrypted_from_email = file.read()
with open('encrypted_smtp_server.bin', 'rb') as file:
    encrypted_smtp_server = file.read()
with open('encrypted_password.bin', 'rb') as file:
    encrypted_password = file.read()

from_email = cipher_suite.decrypt(encrypted_from_email).decode()
smtp_server = cipher_suite.decrypt(encrypted_smtp_server).decode()
smtp_password = cipher_suite.decrypt(encrypted_password).decode()  # Decrypt function

# Function to send email with attachments
def send_email(source_folder, archive_folder, to_emails, subject, body):
    # Create the email message
    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject
    msg.set_content(body, subtype='html')  # Set content type to HTML

    # Attach .txt files from the source folder
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(source_folder, file_name)
            with open(file_path, "rb") as file:
                file_data = file.read()
                file_name = os.path.basename(file_path)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, smtp_password)
            server.send_message(msg)
        logging.info(f"Email sent successfully to {', '.join(to_emails)}")
    except Exception as e:
        logging.error(f"Failed to send email to {', '.join(to_emails)}: {e}")

    # Move files to the archive folder
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".txt"):
            source_path = os.path.join(source_folder, file_name)
            archive_path = os.path.join(archive_folder, file_name)
            os.rename(source_path, archive_path)

# Process each folder configuration
for config in folder_configs:
    send_email(config["source_folder"], config["archive_folder"], config["to_emails"], config["subject"], config["body"])
