import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandface_backend.settings')
django.setup()


from cryptography.fernet import Fernet
print(Fernet.generate_key())
