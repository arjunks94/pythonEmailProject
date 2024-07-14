import smtplib
import os
from email.message import EmailMessage
from cryptography.fernet import Fernet

# Configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
from_email = "opera.ssp@sunsiyam.com"
to_emails = ["arjun.ks@sunsiyam.com", "vishnu.ts@sunsiyam.com"]
subject = "OPERA SSP H&F Reports"
body = "OPERA SSP H&F TR and RR Reports Attached"

#path for windows
source_folder = r"E:\Email\reports"  
archive_folder = r"E:\Email\archive"  

#path for Ubuntu
#source_folder = "/path/to/Email_SSP"  
#archive_folder = "/path/to/Archive"   


# Load the key
with open('key.key', 'rb') as key_file:
    key = key_file.read()

# Initialize the Fernet object with the key
cipher_suite = Fernet(key)

# Load and decrypt the password
with open('encrypted_password.bin', 'rb') as file:
    encrypted_password = file.read()

smtp_password = cipher_suite.decrypt(encrypted_password).decode()  # Decrypt and decode the password

# Create the email message
msg = EmailMessage()
msg["From"] = from_email
msg["To"] = ", ".join(to_emails)
msg["Subject"] = subject
msg.set_content(body)

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
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")

# Move files to the archive folder
for file_name in os.listdir(source_folder):
    if file_name.endswith(".txt"):
        source_path = os.path.join(source_folder, file_name)
        archive_path = os.path.join(archive_folder, file_name)
        os.rename(source_path, archive_path)
