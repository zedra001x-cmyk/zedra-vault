from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

def generate_key(master_password: str, salt: bytes) -> bytes:
    key = hashlib.pbkdf2_hmac(
        'sha256',
        master_password.encode(),
        salt,
        100000
    )
    return key

def encrypt(plaintext: str, key: bytes) -> str:
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = plaintext + ' ' * (16 - len(plaintext) % 16)
    encrypted = cipher.encrypt(padded.encode())
    result = base64.b64encode(iv + encrypted).decode()
    return result

def decrypt(ciphertext: str, key: bytes) -> str:
    raw = base64.b64decode(ciphertext)
    iv = raw[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(raw[16:]).decode()
    return decrypted.strip()
