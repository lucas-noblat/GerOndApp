function enviarDados() {
    // Pegar os valores do formulário
    const amplitude = document.getElementById("entrada-amplitude").value;
    const frequencia = document.getElementById("entrada-frequencia").value;
    const duracao = document.getElementById("entrada-duracao").value;
    const fase = document.getElementById("entrada-fase").value;
    const intervalo = document.getElementById("entrada-intervalo").value;
    const offset = document.getElementById("entrada-offset").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Dados que serão enviados (formato JSON)
    const dados = {
        amplitude: amplitude,
        frequencia: frequencia,
        duracao: duracao,
        fase: fase,
        intervalo: intervalo,
        offset: offset,
    };

    // Configurar a requisição Fetch (POST)
    fetch("/home/", {  
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,  // Proteção CSRF
        },
        body: JSON.stringify(dados),  // Converte objeto em JSON
    })
    .then(response => response.json())  // Converte resposta em JSON
    .then(data => {
        document.getElementById("resposta").innerHTML = data.mensagem;
    })
    .catch(error => console.error("Erro:", error));
}