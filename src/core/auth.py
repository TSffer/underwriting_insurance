import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/users.db")


def init_db():
    """Inicializa la base de datos de usuarios si no existe."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Crear tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'ejecutivo'
        )
    ''')

    # Usuario por defecto: admin/admin123
    try:
        if not check_user_exists(c, "admin"):
            create_user(c, "admin", "admin123", "admin")
            print("✅ Usuario 'admin' creado por defecto.")
    except Exception as e:
        print(f"Info: {e}")

    conn.commit()
    conn.close()


def check_user_exists(cursor, username):
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    return cursor.fetchone() is not None


def create_user(cursor, username, password, role="ejecutivo"):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                   (username, password_hash, role))


def verify_user(username, password):
    """Verifica credenciales. Retorna (bool, role)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    c.execute("SELECT role FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    result = c.fetchone()
    conn.close()

    if result:
        return True, result[0]
    return False, None
