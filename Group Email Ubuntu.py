import os
from cryptography.fernet import Fernet
import yagmail

# Configuration for email
smtp_server = "smtp.gmail.com"
smtp_port = 587
from_email = "opera.ssp@sunsiyam.com"

#path for Ubuntu
#source_folder = "/path/to/Email_SSP"  
#archive_folder = "/path/to/Archive" 

# Paths for Windows
folder_configs = [
    {
        "source_folder": r"E:\Email\reports_group1",  # Use raw string for Windows
        "archive_folder": r"E:\Email\archive_group1",  # Use raw string for Windows
        "to_emails": ["group1@example.com"],
        "subject": "Group 1: OPERA SSP H&F Reports",
        "body": "Group 1: OPERA SSP H&F TR and RR Reports Attached"
    },
    {
        "source_folder": r"E:\Email\reports_group2",  # Use raw string for Windows
        "archive_folder": r"E:\Email\archive_group2",  # Use raw string for Windows
        "to_emails": ["group2@example.com"],
        "subject": "Group 2: OPERA SSP H&F Reports",
        "body": "Group 2: OPERA SSP H&F TR and RR Reports Attached"
    }
]

# Load the key
with open('key.key', 'rb') as key_file:
    key = key_file.read()

# Initialize the Fernet object with the key
cipher_suite = Fernet(key)

# Load and decrypt the password
with open('encrypted_password.bin', 'rb') as file:
    encrypted_password = file.read()

smtp_password = cipher_suite.decrypt(encrypted_password).decode()  # Decrypt and decode the password

# Function to send email with attachments using yagmail
def send_email_yagmail(source_folder, archive_folder, to_emails, subject, body):
    # Initialize yagmail with SMTP server and port
    yag = yagmail.SMTP(user=from_email, password=smtp_password, host=smtp_server, port=smtp_port)

    # List of attachments
    attachments = [os.path.join(source_folder, file_name) for file_name in os.listdir(source_folder) if file_name.endswith(".txt")]

    # Send the email
    try:
        yag.send(to=to_emails, subject=subject, contents=body, attachments=attachments)
        print(f"Email sent successfully to {', '.join(to_emails)}")
    except Exception as e:
        print(f"Failed to send email to {', '.join(to_emails)}: {e}")

    # Move files to the archive folder
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".txt"):
            source_path = os.path.join(source_folder, file_name)
            archive_path = os.path.join(archive_folder, file_name)
            os.rename(source_path, archive_path)

# Process each folder configuration
for config in folder_configs:
    send_email_yagmail(config["source_folder"], config["archive_folder"], config["to_emails"], config["subject"], config["body"])
