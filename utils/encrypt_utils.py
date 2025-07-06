# utils/encrypt_utils.py
from cryptography.fernet import Fernet
from django.conf import settings

# Store this securely (env or settings)
SECRET_KEY = settings.ENCRYPTION_KEY

fernet = Fernet(SECRET_KEY)

def encrypt_response(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_response(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
