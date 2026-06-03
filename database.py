import sqlite3

def init_db():
    conn = sqlite3.connect("logs.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            script TEXT,
            parametros TEXT,
            resultado TEXT,
            status TEXT,
            horario TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT,
            parametros TEXT,
            ativo INTEGER DEFAULT 1
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS config (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO config (chave, valor) 
        VALUES ('token', 'meutoken123')
    """)
    conn.commit()
    conn.close()

def salvar_log(script, parametros, resultado, status):
    conn = sqlite3.connect("logs.db")
    conn.execute(
        "INSERT INTO logs (script, parametros, resultado, status) VALUES (?, ?, ?, ?)",
        (script, parametros, resultado, status)
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

def buscar_scripts():
    conn = sqlite3.connect("logs.db")
    scripts = conn.execute("SELECT * FROM scripts").fetchall()
    conn.close()
    return scripts

def cadastrar_script(nome, descricao, parametros):
    conn = sqlite3.connect("logs.db")
    conn.execute(
        "INSERT INTO scripts (nome, descricao, parametros) VALUES (?, ?, ?)",
        (nome, descricao, parametros)
    )
    conn.commit()
    conn.close()

def alterar_status_script(id, ativo):
    conn = sqlite3.connect("logs.db")
    conn.execute("UPDATE scripts SET ativo=? WHERE id=?", (ativo, id))
    conn.commit()
    conn.close()

def buscar_token():
    conn = sqlite3.connect("logs.db")
    resultado = conn.execute(
        "SELECT valor FROM config WHERE chave='token'"
    ).fetchone()
    conn.close()
    return resultado[0] if resultado else "meutoken123"

def atualizar_token(novo_token):
    conn = sqlite3.connect("logs.db")
    conn.execute(
        "UPDATE config SET valor=? WHERE chave='token'", 
        (novo_token,)
    )
    conn.commit()
    conn.close()