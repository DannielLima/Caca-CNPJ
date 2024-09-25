import requests
from rich.console import Console
from rich.table import Table
from rich.progress import track
import click
import time
import csv
import json
from datetime import datetime, timedelta

cache_cnpj = {}

console = Console()

CACHE_EXPIRATION_DAYS = 7

def validar_cnpj(cnpj):

    if len(cnpj) != 14 or not cnpj.isdigit():
        return False

    def calcula_digito(cnpj, peso):
        soma = sum(int(cnpj[i]) * peso[i] for i in range(len(peso)))
        digito = 11 - soma % 11
        return '0' if digito >= 10 else str(digito)

    primeiro_peso = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    segundo_peso = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    primeiro_digito = calcula_digito(cnpj[:-2], primeiro_peso)
    segundo_digito = calcula_digito(cnpj[:-1], segundo_peso)
    
    return cnpj[-2:] == primeiro_digito + segundo_digito

def get_cnpj_info(cnpj):

    if cnpj in cache_cnpj:
        cache_data = cache_cnpj[cnpj]
        if datetime.now() - cache_data['timestamp'] < timedelta(days=CACHE_EXPIRATION_DAYS):
            console.print(f"[cyan]Recuperando dados do cache para o CNPJ {cnpj}...[/cyan]")
            return cache_data['data']
        else:
            del cache_cnpj[cnpj]

    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Erro ao buscar dados do CNPJ: {str(e)}"

    if response.status_code == 429:
        return "Muitas requisições. Tente novamente mais tarde."

    data = response.json()
    if "estabelecimento" not in data:
        return "Dados do CNPJ não encontrados."

    estabelecimento = data.get("estabelecimento", {})
    
    razao_social = data.get("razao_social", "N/A")
    nome_fantasia = estabelecimento.get("nome_fantasia", "N/A")
    situacao_cadastral = estabelecimento.get("situacao_cadastral", "N/A")
    data_inicio_atividade = estabelecimento.get("data_inicio_atividade", "N/A")
    
    logradouro = estabelecimento.get("logradouro", "N/A")
    numero = estabelecimento.get("numero", "N/A")
    bairro = estabelecimento.get("bairro", "N/A")
    cidade = estabelecimento.get("cidade", {}).get("nome", "N/A")
    estado = estabelecimento.get("estado", {}).get("sigla", "N/A")
    pais = estabelecimento.get("pais", {}).get("nome", "N/A")
    cep = estabelecimento.get("cep", "N/A")
    telefone = estabelecimento.get("telefone1", "N/A")
    email = estabelecimento.get("email", "N/A")
    atividade_principal = estabelecimento.get("atividade_principal", {}).get("descricao", "N/A")

    endereco = f"{logradouro}, {numero} - {bairro}, {cidade} - {estado}, {cep} ({pais})"

    result = {
        "Razão Social": razao_social,
        "Nome Fantasia": nome_fantasia,
        "Situação Cadastral": situacao_cadastral,
        "Data Início Atividade": data_inicio_atividade,
        "Endereço": endereco,
        "Telefone": telefone,
        "Email": email,
        "Atividade Principal": atividade_principal
    }

    cache_cnpj[cnpj] = {'data': result, 'timestamp': datetime.now()}
    return result

def print_results(results):
    console.print("\n[bold green]Informações do CNPJ:[/bold green]\n")
    
    table = Table(show_header=True, header_style="bold cyan", title="[bold yellow]Detalhes do CNPJ[/bold yellow]")
    table.add_column("Campo", style="dim", width=25)
    table.add_column("Valor", style="light_green")

    for key, value in track(results.items(), description="Carregando informações..."):
        table.add_row(key, value)

    console.print(table)

def save_results_to_file(results, filename, file_format):

    if file_format == "csv":
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Campo", "Valor"])
            for key, value in results.items():
                writer.writerow([key, value])
        console.print(f"[bold green]Resultados salvos em {filename}[/bold green]")
    elif file_format == "json":
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
        console.print(f"[bold green]Resultados salvos em {filename}[/bold green]")

@click.command()
@click.option('--cnpj', prompt="Digite o CNPJ (apenas números)", help="CNPJ a ser consultado.")
def main(cnpj):
    console.rule("[bold blue]Consulta de CNPJ[/bold blue]")

    if not validar_cnpj(cnpj):
        console.print("[bold red]CNPJ inválido.[/bold red] Certifique-se de que possui 14 dígitos válidos.")
        return

    results = get_cnpj_info(cnpj)
    
    if isinstance(results, dict):
        print_results(results)
        
        save_choice = console.input("\nDeseja salvar os resultados? [S/N]: ").strip().lower()
        
        if save_choice == 's':
            file_format = console.input("\nEscolha o formato de arquivo (csv/json): ").strip().lower()
            if file_format not in ['csv', 'json']:
                console.print("[bold red]Formato inválido! Escolha entre 'csv' ou 'json'.[/bold red]")
            else:
                filename = f"cnpj_{cnpj}.{file_format}"
                save_results_to_file(results, filename, file_format)
        else:
            console.print("[yellow]Resultados não foram salvos.[/yellow]")
    else:
        console.print(f"[bold red]{results}[/bold red]")

if __name__ == "__main__":
    main()
