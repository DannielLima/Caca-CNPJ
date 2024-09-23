from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/cnpj/{cnpj}", response_class=HTMLResponse)
async def get_cnpj_info(request: Request, cnpj: str):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    response = requests.get(url)
    data = response.json()
    return templates.TemplateResponse("consulta.html", {
        "request": request,
        "nome_fantasia": data.get("nome_fantasia"),
        "cnpj_raiz": data.get("cnpj_raiz"),
        "cnpj_ordem": data.get("cnpj_ordem"),
        "cnpj_digito_verificador": data.get("cnpj_digito_verificador"),
        "situacao_cadastral": data.get("situacao_cadastral"),
        "data_inicio_atividade": data.get("data_inicio_atividade"),
        "tipo_logradouro": data.get("tipo_logradouro"),
        "logradouro": data.get("logradouro"),
        "numero": data.get("numero"),
        "complemento": data.get("complemento"),
        "bairro": data.get("bairro"),
        "cep": data.get("cep"),
        "ddd1": data.get("ddd1"),
        "telefone1": data.get("telefone1"),
        "email": data.get("email"),
        "atividade_principal": data.get("atividade_principal"),
        "atividades_secundarias": data.get("atividades_secundarias", [])
    })