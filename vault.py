from crypto import generate_key, encrypt, decrypt
from database import init_db, add_entry, get_all_entries, get_entry_by_site, delete_entry
from auth import master_exists, save_master, load_master, verify_password
from Crypto.Random import get_random_bytes

class ZedraVault:
    def __init__(self):
        self.key = None
        init_db()

    def setup(self, master_password: str) -> bool:
        if master_exists():
            return False
        salt = get_random_bytes(16)
        save_master(master_password, salt)
        self.key = generate_key(master_password, salt)
        return True

    def login(self, master_password: str) -> bool:
        if not master_exists():
            return False
        data = load_master()
        if verify_password(data["hash"], master_password):
            salt = bytes.fromhex(data["salt"])
            self.key = generate_key(master_password, salt)
            return True
        return False

    def add_password(self, site: str, username: str, password: str, notes: str = "") -> None:
        encrypted = encrypt(password, self.key)
        add_entry(site, username, encrypted, notes)

    def get_passwords(self) -> list:
        entries = get_all_entries()
        result = []
        for row in entries:
            decrypted = decrypt(row[3], self.key)
            result.append({
                "id": row[0],
                "site": row[1],
                "username": row[2],
                "password": decrypted,
                "notes": row[4],
                "created_at": row[5]
            })
        return result

    def search(self, site: str) -> list:
        entries = get_entry_by_site(site)
        result = []
        for row in entries:
            decrypted = decrypt(row[3], self.key)
            result.append({
                "id": row[0],
                "site": row[1],
                "username": row[2],
                "password": decrypted,
                "notes": row[4],
                "created_at": row[5]
            })
        return result

    def delete_password(self, entry_id: int) -> None:
        delete_entry(entry_id)

    def is_unlocked(self) -> bool:
        return self.key is not None
