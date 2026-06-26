import sqlite3

DB_FILE = "vault.db"

def init_db() -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(site: str, username: str, password: str, notes: str = "") -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO passwords (site, username, password, notes) VALUES (?, ?, ?, ?)",
        (site, username, password, notes)
    )
    conn.commit()
    conn.close()

def get_all_entries() -> list:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, site, username, password, notes, created_at FROM passwords")
    rows = c.fetchall()
    conn.close()
    return rows

def get_entry_by_site(site: str) -> list:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT id, site, username, password, notes, created_at FROM passwords WHERE site LIKE ?",
        (f"%{site}%",)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def delete_entry(entry_id: int) -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
