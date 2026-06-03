# ⚡ ISY.ONE — Shell Automation API

> Orquestrador automático de infraestrutura via API REST

---

## 📌 O que é esse projeto?

Uma API que automatiza a execução de scripts bash, eliminando a necessidade de rodar comandos manualmente no terminal a cada novo cliente ou configuração de ambiente.

Em vez de acessar o servidor e digitar comandos na mão, basta fazer uma chamada autenticada à API — ela executa o script, registra o resultado e disponibiliza o histórico completo.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.11 | Linguagem principal |
| FastAPI | Framework da API REST |
| SQLite | Banco de dados para logs e configurações |
| Docker | Containerização da aplicação |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| Uvicorn | Servidor ASGI para rodar o FastAPI |

---

## 📁 Estrutura do projeto

```
api-scripts/
├── scripts/           → pasta com os scripts .sh
│   └── teste.sh
├── .env               → token de segurança
├── database.py        → funções do banco de dados SQLite
├── main.py            → código principal da API
├── index.html         → interface principal
├── admin.html         → painel de administração
├── requirements.txt   → dependências do projeto
└── Dockerfile         → configuração do container Docker
```

---

## ▶️ Como rodar o projeto

### Pré-requisitos

- [Python 3.11+](https://python.org)
- [Docker Desktop](https://docker.com/products/docker-desktop)
- [VS Code](https://code.visualstudio.com) (recomendado)

---

### Opção 1 — Rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/JulioCLSantos/api-scripts.git
cd api-scripts
```

**2. Instale as dependências**
```bash
pip install fastapi uvicorn python-dotenv aiofiles
```

**3. Suba a API**
```bash
uvicorn main:app --reload
```

**4. Acesse no navegador**
```
http://127.0.0.1:8000
```

---

### Opção 2 — Rodar com Docker

**1. Build da imagem**
```bash
docker build -t api-scripts .
```

**2. Rodar o container**
```bash
docker run -p 8000:8000 -v ${PWD}/scripts:/app/scripts api-scripts
```

**3. Acesse no navegador**
```
http://127.0.0.1:8000
```

---

## 🔐 Autenticação

Todas as requisições precisam do token no header:

```
x-isy-token: meutoken123
```

O token pode ser alterado dinamicamente pelo **Painel de Administração** sem necessidade de reiniciar a API.

---

## 🌐 Endpoints disponíveis

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Interface principal |
| GET | `/admin` | Painel de administração |
| GET | `/docs` | Documentação Swagger |
| GET | `/scripts` | Lista os scripts disponíveis |
| POST | `/executar` | Executa um script |
| GET | `/logs` | Histórico de execuções |
| GET | `/admin/scripts` | Lista scripts cadastrados |
| POST | `/admin/scripts` | Cadastra um novo script |
| PUT | `/admin/scripts/{id}` | Ativa ou desativa um script |
| PUT | `/admin/token` | Atualiza o token de autenticação |

---

## 🖥️ Interfaces

### Interface Principal — `http://127.0.0.1:8000`
- Autenticação por token
- Listagem de scripts disponíveis
- Execução de scripts com parâmetros
- Histórico de execuções com status e horário

### Painel de Administração — `http://127.0.0.1:8000/admin`
- Cadastro de scripts com nome, descrição e parâmetros
- Ativar/desativar scripts
- Alteração do token de autenticação

### Swagger — `http://127.0.0.1:8000/docs`
- Documentação interativa gerada automaticamente pelo FastAPI
- Teste dos endpoints diretamente pelo navegador

---

## 🛡️ Segurança

- Autenticação via header `x-isy-token` em todos os endpoints
- Proteção contra **Command Injection** — caracteres especiais (`;`, `&`, `|`, `>`, `<`) são bloqueados no nome do script
- Token armazenado no banco de dados e atualizável sem reinicialização

---

## 📊 Logs e Auditoria

Cada execução é registrada automaticamente no banco SQLite com:
- ID da execução
- Nome do script
- Parâmetros utilizados
- Resultado/output
- Status (`sucesso` ou `falha`)
- Horário da execução

---

## 🚀 Melhorias futuras

- Autenticação avançada com JWT
- Fila de execução para scripts simultâneos
- Interface de monitoramento em tempo real
- Suporte a agendamento de scripts (cron jobs)
- Notificações por e-mail em caso de falha

---

## 👤 Autor

**Julio Cesar** — [github.com/JulioCLSantos](https://github.com/JulioCLSantos)
