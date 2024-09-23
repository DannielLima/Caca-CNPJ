from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Rota para buscar informações do CNPJ
@app.get("/cnpj/{cnpj}")
async def get_cnpj_info(cnpj: str):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    response = requests.get(url)
    return response.json()
