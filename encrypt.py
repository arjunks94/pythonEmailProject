from cryptography.fernet import Fernet
import getpass

# Generate a key and write it to a file
key = Fernet.generate_key()
with open('key.key', 'wb') as key_file:
    key_file.write(key)

# Initialize the Fernet object with the key
cipher_suite = Fernet(key)

# Take user input for the email, SMTP server, and password
from_email = input("Enter the 'From' email address: ").encode()
smtp_server = input("Enter the SMTP server address: ").encode()
password = getpass.getpass("Enter the email password: ").encode()  # Use getpass to hide password input

# Encrypt the email, SMTP server, and password
encrypted_from_email = cipher_suite.encrypt(from_email)
encrypted_smtp_server = cipher_suite.encrypt(smtp_server)
encrypted_password = cipher_suite.encrypt(password)

# Write the encrypted details to files
with open('encrypted_from_email.bin', 'wb') as file:
    file.write(encrypted_from_email)
with open('encrypted_smtp_server.bin', 'wb') as file:
    file.write(encrypted_smtp_server)
with open('encrypted_password.bin', 'wb') as file:
    file.write(encrypted_password)

print("Email, SMTP server, and password encrypted and stored in respective files.")
