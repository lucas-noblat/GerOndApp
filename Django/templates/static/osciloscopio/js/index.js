// CONTROLE DAS ABAS - VERSÃO DEFINITIVA
function iniciarAbas() {
    // Ativa a aba inicial
    const sinalInicial = document.getElementById('numero_sinal').value;
    ativarAba(sinalInicial);
    
    // Configura eventos dos botões
    document.querySelectorAll('.botao-sinal').forEach(btn => {
        btn.addEventListener('click', function() {
            const sinal = this.getAttribute('data-sinal');
            ativarAba(sinal);
        });
    });
    
    // Controle do duty cycle
    document.getElementById('entrada-forma-sinal').addEventListener('change', mostrarDivDuty);
    mostrarDivDuty(); // Configura estado inicial
}


// ATIVAR AS ABAS
function ativarAba(sinal) {

    // Remove classe active de todas as abas
    document.querySelectorAll('.botao-sinal').forEach(aba => {
        aba.classList.remove('active');
        aba.style.border = "";
    });
    
    // Ativa a aba clicada (botão)
    const abaAtiva = document.querySelector(`.botao-sinal[data-sinal="${sinal}"]`);
    if (abaAtiva) {

        abaAtiva.classList.add('active');        
        const coresAbas = {
            1: "2px solid blue",
            2: "2px solid orange",
            3: "2px solid green",
            4: "2px solid red",
            5: "2px solid purple"
        }

        // Define a cor da aba dependendo do sinal, por padrão é azul
        abaAtiva.style.border = coresAbas[sinal] || "2px solid blue";
    }
    
    // Atualiza campo hidden
    document.getElementById('numero_sinal').value = sinal;
    console.log(`Aba ${sinal} ativada`); // Debug
}


function mostrarDivDuty() {
    const forma = document.getElementById('entrada-forma-sinal').value;
    const dutyDiv = document.getElementById('grupo-duty');
    const dutyInput = document.getElementById('entrada-duty');
    

    // Mostra a div do duty apenas se a forma for triangular ou quadrada
    if (forma === "quadrada" || forma === "triangular") {
        dutyDiv.style.display = "flex";
        dutyInput.disabled = false;
        dutyInput.required = true;
        
    } else {
        dutyDiv.style.display = "none";
        dutyInput.disabled = true;
        dutyInput.required = false;
    }
}

function trocarAbas(aba_clicada){
    
    document.querySelectorAll('.aba-btn').forEach(button => {
        button.classList.remove('active');
    });

    document.querySelectorAll('.grafico').forEach(grafico =>{
        grafico.style.display = 'none';
    })


    const aba_ativa = document.querySelector(`.aba-btn#btn-${aba_clicada}`);
    const grafico_ativo = document.querySelector(`.grafico#grafico_${aba_clicada}`)

    if (aba_ativa) {
        aba_ativa.classList.add('active');
    } else {
        window.alert('Essa aba não existe');
    }

    if (grafico_ativo) {
        grafico_ativo.style.display = 'flex';
    } else{
        window.alert('Esse gráfico não existe');
    }

}




// Função para receber dados (BACKEND -> FRONTEND)

function getData(){

        try{
            fetch("http://127.0.0.1:8000/api/getData/")
            .then(response => {
                if(!response.ok){
                    throw new Error ("Não foi possível carregar a API");
                }
                return response.json();})
            .then(dados => {
                console.log(dados.nome);
            })
            .catch(error => {
                console.error(error);
            });
        } catch(error){
            throw error;
        }

}

// Função para enviar dados (FRONTEND -> BACKEND)

async function sendData(){

        const parametros = receberParametros();


        try{
            const response = await fetch("http://127.0.0.1:8000/api/sendData/", {
                method: 'POST',
                headers: { 'Content-Type' : 'application/json'},
                body: JSON.stringify(parametros)
            })

            if(!response.ok){
                throw new Error("Não foi possível resgatar api");}
            
                const dadosNovos = await response.json();
                console.log(dadosNovos);
                return dadosNovos;
        } catch(error){
            throw error;
        }
 
}

// RECEBE OS DADOS DO PARÂMETRO

function receberParametros(){
    const parametros = {
        amplitude: parseFloat(document.getElementById("entrada-amplitude").value),
        rate: parseFloat(document.getElementById("entrada-rate").value),
        frequencia: parseFloat(document.getElementById("entrada-frequencia").value),
        duracao: parseFloat(document.getElementById("entrada-duracao").value),
        fase: parseFloat(document.getElementById("entrada-fase").value),
        offset: parseFloat(document.getElementById("entrada-offset").value),
        operacao: document.getElementById("entrada-operacao").value,
        duty: parseFloat(document.getElementById("entrada-duty").value),
        forma_sinal: document.getElementById("entrada-forma-sinal").value,
        div: document.getElementById("grafico_tempo").innerHTML
    }
    return parametros;
}


// Função assíncrona que irá atualizar os dados

async function atualizarAPI(){

    try{
        const resultadoGetData = await getData();
        console.log(resultadoGetData);
     
        const resultadoSendData = await sendData();
        console.log(resultadoSendData);

        const source = Bokeh.documents[0].get_model_by_name("databaseInternoBokeh");

        if(source && resultadoSendData){            
            source.data.x = resultadoSendData.x;
            source.data.y = resultadoSendData.y;
            source.change.emit();
        }
        else {
            console.warn("Não foi possível atualizar o gráfico: dados ou source não definidos.");
        }
        
    } catch(error){
        console.error(error);
    }

}


// FUNÇÃO PARA ATUALIZAR O GRAFICO

function atualizarGraficoBokeh(dados) {
    const graf = document.getElementById("grafico_tempo");

}


// Inicializa o dom

document.addEventListener('DOMContentLoaded', function() {
    iniciarAbas();
    trocarAbas('tempo');
    atualizarAPI();
});


const amplitude = document.getElementById("entrada-amplitude");

amplitude.addEventListener("change", function() {
    atualizarAPI();
})







