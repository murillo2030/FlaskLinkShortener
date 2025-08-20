import base64
from cryptography.fernet import Fernet
import os




KEY = base64.urlsafe_b64encode(os.urandom(32))

print(KEY.decode())
