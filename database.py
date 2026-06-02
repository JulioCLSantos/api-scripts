import sqlite3

def init_db():
    conn = sqlite3.connect("logs.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            script TEXT,
            parametros TEXT,
            resultado TEXT,
            horario TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def salvar_log(script, parametros, resultado):
    conn = sqlite3.connect("logs.db")
    conn.execute(
        "INSERT INTO logs (script, parametros, resultado) VALUES (?, ?, ?)",
        (script, parametros, resultado)
    )
    conn.commit()
    conn.close()

def buscar_logs():
    conn = sqlite3.connect("logs.db")
    logs = conn.execute(
        "SELECT * FROM logs ORDER BY horario DESC LIMIT 20"
    ).fetchall()
    conn.close()
    return logs