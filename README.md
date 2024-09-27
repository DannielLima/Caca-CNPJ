
# Caça-CNPJ

Caça-CNPJ é uma ferramenta de linha de comando para consultar informações de CNPJ utilizando a API pública de CNPJ.

## Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/DannielLima/Caca-CNPJ.git
```

2. **Navegue até o diretório do projeto:**

```bash
cd Caca-CNPJ
```

3. **Crie um ambiente virtual (opcional, mas recomendado):**

#### No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### No Linux/MacOS:

```bash
python -m venv venv
source venv/bin/activate
```

4. **Instale as dependências:**

```bash
pip install .
```
## Uso

Após instalar as dependências, execute o programa com o seguinte comando:

```bash
cacacnpj
```
O programa pedirá que você insira o CNPJ para realizar a consulta:

```bash
Digite o CNPJ (apenas números): 
```
## Exemplo de Execução:

```bash
$ cacacnpj
Digite o CNPJ (apenas números): 12345678000195

Informações do CNPJ:

Razão Social: Exemplo Empresa Ltda
Nome Fantasia: Exemplo Fantasia
Situação Cadastral: Ativa
Data Início Atividade: 01/01/2000
Endereço: Rua Exemplo, 123 - Bairro Exemplo, Cidade - Estado, 00000-000 (Brasil)
Telefone: (11) 1234-5678
Email: contato@empresaexemplo.com.br
Atividade Principal: Comércio Varejista de Produtos Diversos
```


## Funcionalidades Adicionais

- **Cache de consultas:** CNPJs consultados recentemente são armazenados em cache por 7 dias.
- **Opção de salvar resultados:** Você pode salvar os resultados em arquivos CSV ou JSON.

Durante a execução, o programa perguntará se deseja salvar os resultados. Basta escolher o formato de arquivo (CSV ou JSON) para armazenar as informações.
