import hashlib
import random

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_otp() -> str:
    return str(random.randint(1000, 9999))
