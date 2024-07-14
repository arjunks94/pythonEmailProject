from cryptography.fernet import Fernet

# Generate a key and write it to a file
key = Fernet.generate_key()
with open('key.key', 'wb') as key_file:
    key_file.write(key)

# Initialize the Fernet object with the key
cipher_suite = Fernet(key)

# Encrypt the password
password = "njzyfdajfagyqzzp".encode()  # Convert the password to bytes
encrypted_password = cipher_suite.encrypt(password)

# Write the encrypted password to a file
with open('encrypted_password.bin', 'wb') as file:
    file.write(encrypted_password)

print("Password encrypted and stored in 'encrypted_password.bin'")

