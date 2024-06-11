<?php
// Função para consultar CNPJ
function consultarCNPJ(string $cnpj): ?array
{
    $cnpj = limparCNPJ($cnpj); // Limpar o CNPJ antes de usar

    $url = "https://publica.cnpj.ws/cnpj/{$cnpj}";

    $curl = curl_init($url);
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

    // For debug only!
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);

    $resp = curl_exec($curl);
    curl_close($curl);

    $dados = json_decode($resp, true);

    // Se houver erro na resposta ou o CNPJ não existir, retorna null
    if (isset($dados['erro'])) {
        return null;
    }

    // Verifica se a resposta indica "Muitas requisições"
    if (isset($dados['status']) && $dados['status'] === 429) {
        return ['status' => 429, 'titulo' => 'Muitas requisições', 'detalhes' => $dados['detalhes']];
    }

    return $dados;
}

// Função para limpar CNPJ
function limparCNPJ(string $cnpj): string
{
    return preg_replace('/[^0-9]/', '', $cnpj);
}

function toUpper($string): string
{
    return mb_strtoupper($string, 'UTF-8');
}

// Verifica se o CNPJ foi passado via GET
if (isset($_GET['cnpj'])) {
    $cnpj = $_GET['cnpj'];
    $dadosCNPJ = consultarCNPJ($cnpj);

    header('Content-Type: application/json');
    echo json_encode($dadosCNPJ);
}
?>