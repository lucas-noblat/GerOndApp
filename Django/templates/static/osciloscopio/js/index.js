function enviarDados() {
    // Pegar os valores do formulário
    const nome = document.getElementById("nome").value;
    const idade = document.getElementById("idade").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Dados que serão enviados (formato JSON)
    const dados = {
        nome: nome,
        idade: idade,
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