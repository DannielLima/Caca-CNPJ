<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Caça-CNPJ 🔎</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
    <link rel="stylesheet" href="assets/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <section class="section">
        <div class="container is-flex is-justify-content-center">
            <div class="box">
                <h1 class="title is-centered">
                    Caça-CNPJ <span class="search-icon" id="searchIcon">🔎</span>
                </h1>
                <form id="cnpjForm">
                    <div class="field">
                        <label class="label" for="cnpj">Digite o CNPJ:</label>
                        <div class="control">
                            <input class="input" type="text" id="cnpj" name="cnpj" placeholder="Digite o CNPJ" required>
                        </div>
                    </div>
                    <div class="field is-grouped">
                        <div class="control">
                            <button class="button is-info" type="submit">Pesquisar</button>
                        </div>
                        <div class="control" id="clearButtonContainer" style="display: none;">
                            <button class="button is-danger" type="button" id="clearButton">Limpar</button>
                        </div>
                    </div>
                </form>
                <div id="resultado"></div>
            </div>
        </div>
    </section>

    <script>
        const searchIcon = document.getElementById('searchIcon');
        let isMoving = false;

        searchIcon.addEventListener('click', function() {
            if (!isMoving) {
                isMoving = true;
                this.style.transform = 'translateX(calc(-100% - 150px))'; // Move a lupa para a esquerda
                setTimeout(() => {
                    this.style.transform = 'translateX(0)'; // Retorna a lupa à sua posição original
                    isMoving = false;
                }, 1000);
            }
        });

        document.getElementById('cnpjForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const cnpj = document.getElementById('cnpj').value;

            fetch('pesquisa.php?cnpj=' + cnpj)
                .then(response => response.json())
                .then(data => {
                    const resultadoDiv = document.getElementById('resultado');
                    resultadoDiv.innerHTML = '';

                    if (data.status === 429) {
                        resultadoDiv.innerHTML = `<div class='notification is-danger'>${data.titulo}: ${data.detalhes}</div>`;
                    } else if (data.razao_social) {
                        let enderecoCNPJ = formatarEndereco(data.estabelecimento);

                        let resultadoHTML = `
                            <div class='content'>
                                <h2 class='subtitle'>Dados do CNPJ (${cnpj})</h2>
                                <p><strong>Razão Social:</strong> ${data.razao_social.toUpperCase()}</p>
                                <p><strong>Nome Fantasia:</strong> ${data.estabelecimento.nome_fantasia ? data.estabelecimento.nome_fantasia.toUpperCase() : "NÃO DISPONÍVEL"}</p>
                                <p><strong>Atividade Principal:</strong> ${data.atividade_principal ? data.atividade_principal.toUpperCase() : "NÃO DISPONÍVEL"}</p>
                                <p><strong>Endereço:</strong> ${enderecoCNPJ}</p>
                                <p><strong>Situação Cadastral:</strong> ${data.estabelecimento.situacao_cadastral ? data.estabelecimento.situacao_cadastral.toUpperCase() : "NÃO DISPONÍVEL"}</p>
                            </div>
                        `;

                        if (data.estabelecimento.cep && data.estabelecimento.bairro) {
                            fetch('consulta_cep.php?cep=' + data.estabelecimento.cep)
                                .then(response => response.json())
                                .then(cepData => {
                                    if (cepData && !cepData.erro) {
                                        let enderecoCEP = formatarEnderecoCEP(cepData, data.estabelecimento.bairro);
                                        resultadoHTML += `
                                            <h2 class='subtitle' style='color: #000;'>Endereço do CEP (${data.estabelecimento.cep})</h2>
                                            <p><strong>Endereço:</strong> ${enderecoCEP}</p>
                                        `;
                                    }
                                    resultadoDiv.innerHTML = resultadoHTML;
                                    document.getElementById('clearButtonContainer').style.display = 'flex';
                                })
                                .catch(error => {
                                    console.error('Erro:', error);
                                    resultadoDiv.innerHTML = resultadoHTML;
                                    document.getElementById('clearButtonContainer').style.display = 'flex';
                                });
                        } else {
                            resultadoDiv.innerHTML = resultadoHTML;
                            document.getElementById('clearButtonContainer').style.display = 'flex';
                        }
                    } else {
                        resultadoDiv.innerHTML = "<div class='notification is-danger'>CNPJ não encontrado.</div>";
                    }
                })
                .catch(error => console.error('Erro:', error));
        });

        document.getElementById('clearButton').addEventListener('click', function() {
            document.getElementById('cnpj').value = '';
            document.getElementById('resultado').innerHTML = '';
            document.getElementById('clearButtonContainer').style.display = 'none';
        });

        function formatarEndereco(estabelecimento) {
            const tipo_logradouro = estabelecimento.tipo_logradouro ? estabelecimento.tipo_logradouro.toUpperCase() : "";
            const logradouro = estabelecimento.logradouro ? estabelecimento.logradouro.toUpperCase() : "";
            const numero = estabelecimento.numero ? estabelecimento.numero : "";
            const complemento = estabelecimento.complemento ? estabelecimento.complemento : "";
            const bairro = estabelecimento.bairro ? estabelecimento.bairro.toUpperCase() : "";
            const cidade = estabelecimento.cidade.nome ? estabelecimento.cidade.nome.toUpperCase() : "";
            const estado = estabelecimento.estado.sigla ? estabelecimento.estado.sigla.toUpperCase() : "";

            const enderecoCompleto = `${tipo_logradouro} ${logradouro}, ${numero} ${complemento} - ${bairro}, ${cidade}, ${estado}`;
            return enderecoCompleto.trim() !== ", , -" ? enderecoCompleto : "NÃO DISPONÍVEL";
        }

        function formatarEnderecoCEP(cepData, bairro) {
            const logradouro = cepData.logradouro ? cepData.logradouro.toUpperCase() : "";
            const localidade = cepData.localidade ? cepData.localidade.toUpperCase() : "";
            const uf = cepData.uf ? cepData.uf.toUpperCase() : "";

            const enderecoCEPCompleto = `${logradouro}, ${bairro.toUpperCase()}, ${localidade}, ${uf}`;
            return enderecoCEPCompleto.trim() !== ", , ," ? enderecoCEPCompleto : "NÃO DISPONÍVEL";
        }
    </script>
</body>
</html>
