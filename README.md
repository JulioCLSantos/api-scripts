# API de Execução de Scripts

## O que é esse projeto?
Uma API que executa scripts automaticamente, sem precisar digitar comandos manualmente no terminal.

## Tecnologias utilizadas
- Python
- FastAPI
- SQLite
- Docker

## Como rodar o projeto

### PASSO 1 — Clone o projeto
git clone https://github.com/JulioCLSantos/api-scripts.git
cd api-scripts

### PASSO 2 — Instale as dependências
pip install fastapi uvicorn python-dotenv

### PASSO 3 — Rode localmente
uvicorn main:app --reload

### PASSO 4 — Ou rode com Docker
docker build -t api-scripts .
docker run -p 8000:8000 api-scripts

### PASSO 5 — Acesse
http://localhost:8000/docs

## Como usar
Use o token no header:
token: meutoken123

## Endpoints
| Método | Endpoint | O que faz |
|---|---|---|
| GET | /scripts | Lista os scripts |
| POST | /executar | Executa um script |
| GET | /logs | Ver histórico |