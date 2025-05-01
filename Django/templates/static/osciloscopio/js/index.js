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
            carregarParametrosSinal(sinal);
            atualizarAPI();
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

        // Atualiza a URL sem recarregar a página
        const url = new URL(window.location);
        url.searchParams.set('sinal', sinal);
        window.history.pushState({}, '', url);
    }
    
    // Atualiza campo hidden
    document.getElementById('numero_sinal').value = sinal;
    //console.log(`Aba ${sinal} ativada`); // Debug
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

async function getData(sinal){

        try{
            const response = await fetch(`http://127.0.0.1:8000/api/getData/?sinal=${sinal}`);

            if(!response.ok){
                throw new Error ("Não foi possível carregar a API");
            }

            return response.json();
     
        } catch(error){
            console.error(error);
        }

}

// Função para enviar dados (FRONTEND -> BACKEND)

async function sendData(sinal){

        const parametros = receberParametros();


        try{
            const response = await fetch(`http://127.0.0.1:8000/api/sendData/?sinal=${sinal}`, {
                method: 'POST',
                headers: { 'Content-Type' : 'application/json'},
                body: JSON.stringify(parametros)
            })

            if(!response.ok){
                throw new Error("Não foi possível resgatar api");}

            return await response.json();
        } catch(error){
            throw error;
        }
 
}

async function carregarParametrosSinal(sinal){
    try{
        const dados = await getData(sinal);

        //console.log(`FORMA SINAL = ${dados['forma_sinal']}`);

        document.getElementById("entrada-amplitude").value = dados['amplitude'];
        document.getElementById("entrada-frequencia").value = dados['frequencia'];
        document.getElementById("entrada-fase").value = dados['fase'];
        document.getElementById("entrada-offset").value = dados['offset'];
        document.getElementById("entrada-forma-sinal").value = dados['forma_sinal'];
        document.getElementById("entrada-operacao").value = dados['operacao'];
        document.getElementById("entrada-duty").value = dados['duty'];
    
        document.getElementById("entrada-duracao").value = dados['duracao'];
        document.getElementById("entrada-rate").value = dados['rate'];

    }
    catch(error){
        console.error(error);
    }
}

// RECEBE OS DADOS DO PARÂMETRO

function receberParametros(){

    const sinal = document.getElementById('numero_sinal').value;
    console.log(document.getElementById("entrada-fase").value);

    const parametros = {
        id: sinal,
        amplitude: parseFloat(document.getElementById("entrada-amplitude").value),
        rate: parseFloat(document.getElementById("entrada-rate").value),
        frequencia: parseFloat(document.getElementById("entrada-frequencia").value),
        duracao: parseFloat(document.getElementById("entrada-duracao").value),
        fase: parseFloat(document.getElementById("entrada-fase").value),
        offset: parseFloat(document.getElementById("entrada-offset").value),
        operacao: document.getElementById("entrada-operacao").value,
        duty: parseFloat(document.getElementById("entrada-duty").value),
        forma_sinal: document.getElementById("entrada-forma-sinal").value}
    return parametros;
}


// Função assíncrona que irá atualizar os dados

async function atualizarAPI(){

    const sinal =document.getElementById('numero_sinal').value || "1";

    try{

 
        const resultadoGetData = await getData(sinal);
        console.log(resultadoGetData);
     
        const resultadoSendData = await sendData(sinal);
        //console.log(resultadoSendData);

        console.log(`databaseInternoBokeh${sinal-1}`);
        const source = Bokeh.documents[0].get_model_by_name(`databaseInternoBokeh${sinal-1}`);

        //console.log(resultadoSendData['amplitude']);

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


// FUNÇÃO PARA ATIVAR OS LISTENERS

function startListeners() {
    const inputs = document.querySelectorAll("input");
    const selects = document.querySelectorAll("select");
    const sinal = parseInt(document.getElementById("numero_sinal").value);

    inputs.forEach(input => {
        input.addEventListener("input", function() {
            //console.log(input.id);
            atualizarAPI();
        })
    })
    
    selects.forEach(select => {
        select.addEventListener("change", function(){
            atualizarAPI();
        })
    })
}


// Inicializa o dom

document.addEventListener('DOMContentLoaded', function() {
    iniciarAbas();
    trocarAbas('tempo');
    startListeners();
    atualizarAPI();
});










