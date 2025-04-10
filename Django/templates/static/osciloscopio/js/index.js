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



    function atualizarCamposDinamicos() {
        const forma_sinal = document.getElementById('entrada-forma-sinal').value;
        const campo_dinamico = document.getElementById('campo-dinamico');

        if (forma_sinal === 'quadrada' || forma_sinal === 'triangular'){
            campo_dinamico.innerHTML = `
            <!-- Duração -->
                <div class="form-group" id="grupo-duracao">
                    <label for="entrada-duracao" class="form-label">Duty</label>
                    <div class="form-number">
                        <input type="number" name="entrada-duracao" id="entrada-duracao" min= 0 max = 100 value = {{duracao}}  value = 1 required>
                    </div>            
                </div>`; 

        } else{
            campo_dinamico.innerHTML = '';
        }

    }

    // 2. Configurar o event listener quando a página carregar
    document.addEventListener('DOMContentLoaded', function() {
        // Obter o elemento select
        const selectSinal = document.getElementById('entrada-forma-sinal');
        
        // Verificar se o elemento existe antes de adicionar o listener
        if (selectSinal) {
            // Adicionar o listener para o evento 'change'
            selectSinal.addEventListener('change', atualizarCamposDinamicos);
            
            // Chamar a função uma vez para inicializar o estado
            atualizarCamposDinamicos();
        } else {
            console.error('Elemento com ID "entrada-forma-sinal" não encontrado!');
        }
    });


  
