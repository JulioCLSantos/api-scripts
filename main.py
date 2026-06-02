import subprocess, os
from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv
from database import init_db, salvar_log, buscar_logs

load_dotenv()
init_db()

app = FastAPI()
TOKEN = os.getenv("TOKEN")

def verificar_token(token: str = Header()):
    if token != TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/scripts")
def listar_scripts(token: str = Header()):
    verificar_token(token)
    arquivos = os.listdir("scripts")
    return {"scripts": [f for f in arquivos if f.endswith(".sh")]}

@app.post("/executar")
def executar_script(nome: str, parametros: str = "", token: str = Header()):
    verificar_token(token)
    caminho = f"scripts/{nome}"
    if not os.path.exists(caminho):
        raise HTTPException(status_code=404, detail="Script não encontrado")
    resultado = subprocess.run(
        ["bash", caminho] + parametros.split(),
        capture_output=True, text=True
    )
    saida = resultado.stdout or resultado.stderr
    salvar_log(nome, parametros, saida)
    return {"resultado": saida}

@app.get("/logs")
def ver_logs(token: str = Header()):
    verificar_token(token)
    logs = buscar_logs()
    return {"logs": logs}