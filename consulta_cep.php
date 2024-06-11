<?php
// Função para consultar CEP usando ViaCEP
function consultarCEP(string $cep): ?array
{
    $cep = limparCEP($cep);

    $url = "https://viacep.com.br/ws/{$cep}/json/";

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $conteudo = curl_exec($ch);
    if (curl_errno($ch)) {
        echo json_encode(['erro' => curl_error($ch)]);
        curl_close($ch);
        return null;
    }
    curl_close($ch);

    $dados = json_decode($conteudo, true);

    // Se houver erro na resposta ou o CEP não existir, retorna null
    if (isset($dados['erro'])) {
        return null;
    }

    return $dados;
}

function limparCEP(string $cep): string
{
    return preg_replace('/[^0-9]/', '', $cep);
}

// Verifica se o CEP foi passado via GET
if (isset($_GET['cep'])) {
    $cep = $_GET['cep'];
    $dadosCEP = consultarCEP($cep);

    header('Content-Type: application/json');
    echo json_encode($dadosCEP);
}
?>