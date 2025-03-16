from cryptography.fernet import Fernet
from flask import current_app

def encrypt_message(message):
    fernet = Fernet(current_app.config['SECRET_KEY'])
    encrypted_message = fernet.encrypt(message.encode())  # Convert string to bytes before encryption
    return encrypted_message


# Decrypt a message (bytes) - decode bytes back to string
def decrypt_message(encrypted_message):
    fernet = Fernet(current_app.config['SECRET_KEY'])
    decrypted_message = fernet.decrypt(encrypted_message).decode()  # Convert bytes to string
    return decrypted_message
