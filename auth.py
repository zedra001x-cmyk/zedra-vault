import argon2
import os
import json

MASTER_FILE = "master.json"

def hash_password(password: str) -> str:
    ph = argon2.PasswordHasher()
    return ph.hash(password)

def verify_password(stored_hash: str, password: str) -> bool:
    ph = argon2.PasswordHasher()
    try:
        return ph.verify(stored_hash, password)
    except argon2.exceptions.VerifyMismatchError:
        return False

def master_exists() -> bool:
    return os.path.exists(MASTER_FILE)

def save_master(password: str, salt: bytes) -> None:
    hashed = hash_password(password)
    data = {
        "hash": hashed,
        "salt": salt.hex()
    }
    with open(MASTER_FILE, "w") as f:
        json.dump(data, f)

def load_master() -> dict:
    with open(MASTER_FILE, "r") as f:
        return json.load(f)
