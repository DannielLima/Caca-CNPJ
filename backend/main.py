from fastapi import FastAPI, Request, HTTPException
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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("consulta.html", {"request": request})

@app.get("/cnpj/{cnpj}", response_class=HTMLResponse)
async def get_cnpj_info(request: Request, cnpj: str):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    response = requests.get(url)

    if response.status_code == 429:
        error_data = response.json()
        message = error_data.get("detalhes", "Erro desconhecido. Tente novamente mais tarde.")
        return templates.TemplateResponse("consulta.html", {
            "request": request,
            "error_message": f"Muitas requisições: {message}",
            "nome_fantasia": None,
            "razao_social": None,
            "cnpj_raiz": None,
            "cnpj_ordem": None,
            "cnpj_digito_verificador": None,
            "situacao_cadastral": None,
            "data_inicio_atividade": None,
            "tipo_logradouro": None,
            "logradouro": None,
            "numero": None,
            "bairro": None,
            "cep": None,
            "ddd1": None,
            "telefone1": None,
            "email": None,
            "atividade_principal": None,
            "atividades_secundarias": []
        })

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erro ao buscar dados do CNPJ.")
    
    data = response.json()
    
    razao_social = data.get("razao_social", "N/A")
    estabelecimento = data.get("estabelecimento", {})
    atividade_principal = estabelecimento.get("atividade_principal", {}).get("descricao", "N/A")
    atividades_secundarias = estabelecimento.get("atividades_secundarias", [])
    
    return templates.TemplateResponse("consulta.html", {
    "request": request,
    "razao_social": razao_social,
    "nome_fantasia": estabelecimento.get("nome_fantasia"),
    "cnpj_raiz": estabelecimento.get("cnpj_raiz"),
    "cnpj_ordem": estabelecimento.get("cnpj_ordem"),
    "cnpj_digito_verificador": estabelecimento.get("cnpj_digito_verificador"),
    "situacao_cadastral": estabelecimento.get("situacao_cadastral"),
    "data_inicio_atividade": estabelecimento.get("data_inicio_atividade"),
    "tipo_logradouro": estabelecimento.get("tipo_logradouro"),
    "logradouro": estabelecimento.get("logradouro"),
    "numero": estabelecimento.get("numero"),
    "bairro": estabelecimento.get("bairro"),
    "cep": estabelecimento.get("cep"),
    "ddd1": estabelecimento.get("ddd1"),
    "telefone1": estabelecimento.get("telefone1"),
    "email": estabelecimento.get("email"),
    "atividade_principal": atividade_principal,
    "atividades_secundarias": atividades_secundarias,
    "cidade": estabelecimento.get("cidade", {}),
    "estado": estabelecimento.get("estado", {}),
    "pais": estabelecimento.get("pais", {})
})
