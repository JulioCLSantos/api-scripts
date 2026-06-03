import subprocess, os
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from database import (init_db, salvar_log, buscar_logs, buscar_scripts,
                      cadastrar_script, alterar_status_script,
                      buscar_token, atualizar_token)

load_dotenv()
init_db()

app = FastAPI(title="Isy.One Shell Automation API", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def verificar_token(x_isy_token: str = Header(...)):
    token_atual = buscar_token()
    if x_isy_token != token_atual:
        raise HTTPException(status_code=401, detail="Token Inválido ou Ausente!")

class ScriptInput(BaseModel):
    nome: str
    descricao: str
    parametros: str = ""

class TokenInput(BaseModel):
    novo_token: str

@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/admin")
def admin():
    return FileResponse(os.path.join(BASE_DIR, "admin.html"))

@app.get("/scripts")
def listar_scripts(x_isy_token: str = Header(...)):
    verificar_token(x_isy_token)
    arquivos = os.listdir(os.path.join(BASE_DIR, "scripts"))
    return {"scripts": [f for f in arquivos if f.endswith(".sh")]}

@app.post("/executar")
def executar_script(nome: str, parametros: str = "", x_isy_token: str = Header(...)):
    verificar_token(x_isy_token)
    if any(c in nome for c in [";", "&", "|", ">", "<", "`", "$"]):
        raise HTTPException(status_code=400, detail="Caracteres inválidos!")
    caminho = os.path.join(BASE_DIR, "scripts", nome)
    if not os.path.exists(caminho):
        raise HTTPException(status_code=404, detail="Script não encontrado!")
    resultado = subprocess.run(
        ["bash", caminho] + parametros.split(),
        capture_output=True, text=True
    )
    saida = resultado.stdout or resultado.stderr
    status = "sucesso" if resultado.returncode == 0 else "falha"
    salvar_log(nome, parametros, saida, status)
    return {"status": status, "resultado": saida}

@app.get("/logs")
def ver_logs(x_isy_token: str = Header(...)):
    verificar_token(x_isy_token)
    logs = buscar_logs()
    return {"logs": logs}

@app.get("/admin/scripts")
def listar_scripts_admin(x_isy_token: str = Header(...)):
    verificar_token(x_isy_token)
    return {"scripts": buscar_scripts()}

@app.post("/admin/scripts")
def novo_script(script: ScriptInput, x_isy_token: str = Header(...)):
    verificar_token(x_isy_token)
    cadastrar_script(script.nome, script.descricao, script.parametros)
    return {"mensagem": "Script cadastrado com sucesso!"}

@app.put("/admin/scripts/{id}")
def toggle_script(id: int, ativo: int, x_isy_token: str = Header(...)):
    verificar_token(x_isy_token)
    alterar_status_script(id, ativo)
    return {"mensagem": "Status atualizado!"}

@app.put("/admin/token")
def alterar_token(dados: TokenInput, x_isy_token: str = Header(...)):
    verificar_token(x_isy_token)
    atualizar_token(dados.novo_token)
    return {"mensagem": "Token atualizado com sucesso!"}