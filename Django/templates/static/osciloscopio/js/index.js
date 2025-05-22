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
            //atualizarAPI();                                     // NO LINUX(OU FIREFOX) faz com que os arquivos sejam atualizados sempre com a mudança da aba

        });
    });
    
    // Controle do duty cycle
    document.getElementById('entrada-forma-sinal').addEventListener('change', mostrarDivDuty);
    mostrarDivDuty(); // Configura estado inicial


}


// ATIVAR AS ABAS
function ativarAba(sinal) {

    document.getElementById(`sinal${sinal}`).checked = true;

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
    aba_ativa ? aba_ativa.classList.add('active') : window.alert('Essa aba não existe');

    if(aba_clicada !== "ambos"){   
        const grafico_ativo = document.querySelector(`.grafico#grafico_${aba_clicada}`);
    
       
        
        grafico_ativo ? grafico_ativo.style.display = 'flex' : window.alert('Esse gráfico não existe');
        grafico_ativo ? grafico_ativo.style.height = '100%' : window.alert("Esse gráfico não existe");
    } else { // ABA AMBOS




        const areaGrafico = document.getElementById("area-grafico");

        graficos = document.querySelectorAll(".grafico");

        graficos.forEach(grafico => {
            if(grafico){
                grafico.style.display = 'flex';
                grafico.style.height = "50%";
                grafico.style.margin = "10px";
            }
        });
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
        if(dados['forma_sinal'] == "senoidal" || dados['forma_sinal'] == "ruido-branco"){
            document.getElementById("grupo-duty").style.display = "None";
            document.getElementById("entrada-duty").disabled = true;

        }
        else{
            document.getElementById("grupo-duty").style.display = "flex";
            document.getElementById("entrada-duty").disabled = false;

        }

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
    //console.log(`Sinal ${sinal} ativo? ` + document.getElementById(`sinal${sinal}`).checked);

    const parametros = {
        id: sinal,
        amplitude: parseFloat(document.getElementById("entrada-amplitude").value),
        rate: parseFloat(document.getElementById("entrada-rate").value),
        frequencia: parseFloat(document.getElementById("entrada-frequencia").value),
        duracao: parseFloat(document.getElementById("entrada-duracao").value),
        fase: parseFloat(document.getElementById("entrada-fase").value) * (Math.PI/180.0),
        offset: parseFloat(document.getElementById("entrada-offset").value),
        operacao: document.getElementById("entrada-operacao").value,
        duty: parseFloat(document.getElementById("entrada-duty").value) || 0.5,
        forma_sinal: document.getElementById("entrada-forma-sinal").value,
        ativo: (document.getElementById(`sinal${sinal}`).checked),
        sinaisAtivos: get_sinaisAtivos()}

    console.log(`Formato do sinal ${sinal} = ${parametros['forma_sinal']}`);
    return parametros;
}

function receberUnidades(){ 
    return {
        amplitude: document.getElementById("unidade-amplitude").value,
        tempo: document.getElementById("unidade-duracao").value,
        frequencia: document.getElementById("unidade-frequencia").value,
    };
}

function get_sinaisAtivos(){
    return [
        (document.getElementById(`sinal1`).checked),
        (document.getElementById(`sinal2`).checked),
        (document.getElementById(`sinal3`).checked),
        (document.getElementById(`sinal4`).checked),
        (document.getElementById(`sinal5`).checked)
    ]
}

// Função assíncrona que irá atualizar os dados

async function atualizarAPI(){

    const sinal =document.getElementById('numero_sinal').value || "1";


    try{

        // Atualizando as unidades

        //Bokeh.documents[0].get_model_by_name("Tempo").left[0].axis_label = `Tempo(${unidades['tempo']})`;

 
        //const resultadoGetData = await getData(sinal);
        //console.log(resultadoGetData);
     
        const resultadoSendData = await sendData(sinal);
        //console.log(resultadoSendData);

        atualizarUnidades();
        atualizarSteps();
        
        for(let i = 0; i < 6; i++){

            //console.log(`Sinal ${i+1}ativo: ${resultadoSendData[i].ativo}`);
            resultadoSendData[i].ativo = i !== 5 ? (document.getElementById(`sinal${i+1}`).checked ? true : false) : true;
            

            if(resultadoSendData[i].ativo == true){
                            const source = Bokeh.documents[0].get_model_by_name(`databaseInternoBokeh${i}`);
                            const sourceFreq = Bokeh.documents[1].get_model_by_name(`dbf${i}`);                
                                    
                            if(source && resultadoSendData && sourceFreq){            
                                source.data.x = resultadoSendData[i].x;
                                source.data.y = resultadoSendData[i].y;

                                
                                sourceFreq.data = {
                                    x: resultadoSendData[i]['xFreq'],
                                    y: resultadoSendData[i]['yFreq']
                                }
                                source.change.emit();

                                if(i !== 5) {
                                    document.getElementById(`cs${i+1}`).style.display = "flex";
                                }
                
                            }
                            else {
                                console.warn("Não foi possível atualizar o gráfico: dados ou source não definidos.");
                            }
            } else {
                const source = Bokeh.documents[0].get_model_by_name(`databaseInternoBokeh${i}`);
                const sourceFreq = Bokeh.documents[1].get_model_by_name(`dbf${i}`);

                if(source && resultadoSendData && sourceFreq){            
                    source.data.x = [];
                    source.data.y = [];
                    
                    sourceFreq.data = {
                        x: [],
                        y: []
                    }
                    source.change.emit();
                }
            }
        }
        
    } catch(error){
        console.error(error);
    }

}


// FUNÇÃO QUE ATUALIZA UNIDADES

function atualizarUnidades(){

    const unidades = receberUnidades();

    const grafTempo = Bokeh.documents[0].get_model_by_name("Tempo");
    const grafFreq = Bokeh.documents[1].get_model_by_name("Frequencia");

    //grafFreq && grafTempo ? console.log("Achei") : console.log("Não encontrado");

    if(grafFreq && grafTempo) {
        grafTempo.left[0].axis_label = `Amplitude(${unidades['amplitude']})`;
        grafTempo.below[0].axis_label = `Tempo(${unidades['tempo']})`;

        grafFreq.left[0].axis_label = `Magnitude(${unidades['amplitude']})`;
        grafFreq.below[0].axis_label = `Frequencia(${unidades['frequencia']})`;

    }
    else {
        console.warning("Gráficos não encontrados");
    }




}

// FUNÇÃO PARA ATUALIZAR OS STES DOS INPUTS

function atualizarSteps(){

    document.querySelectorAll('input[type = "number"').forEach(input => {

        // Atualização do step dos inputs (Pedido do Fábio)

        if(!isNaN(input.value && input.value.trim() !== '')){
            if(input.value.includes('.') || input.value.includes(','))
            {
                input.step = 0.1;
            } else {
                input.step = 1;
            }
        }
        })
}


// FUNÇÃO PARA ATIVAR OS LISTENERS

function startListeners() {
    const inputs = document.querySelectorAll("input");
    const selects = document.querySelectorAll("select");
    const radios = document.querySelectorAll('input[type="radio"]');


    const abas_config_sobre = document.querySelectorAll(".container-aba");

    const overLayerPopup = document.getElementById("blur-popup");
    const popup = document.getElementById("popup-config");
    const fechar_popup = document.getElementById("fechar-popup");


    function posicionarPopup(aba){
        const retangulo = aba.getBoundingClientRect();

        const posX = retangulo.right + 10;
        const posY = retangulo.top;

        popup.style.left = `${posX}px`;
        popup.style.top = `${posY}px`;

        popup.style.opacity = 1;
        popup.style.visibility = "visible";


    }


    // TODOS OS INPUTS NUMÉRICOS
    inputs.forEach(input => {
        input.addEventListener("input", function() {
            //console.log(input.id);
            atualizarAPI();
        })
    });
    

    // TODOS OS INPUT DO TIPO SELECT
    selects.forEach(select => {
        select.addEventListener("change", function(){
            atualizarAPI();
        })
    });

    // EVENTOS ABA DA ESQUERDA

    abas_config_sobre.forEach(aba => {
        aba.addEventListener("click", function(){

            posicionarPopup(aba);

            overLayerPopup.style.transition = "all 0.4 ease";
    
            overLayerPopup.style.opacity = 0.6;
            overLayerPopup.style.visibility = "visible";
            aba.classList.add('active');
    
        });
    });
    // ABA DE CONFIGURAÇÕES


    fechar_popup.onclick = function () {
        overLayerPopup.style.opacity = 0;
        overLayerPopup.style.visibility = "hidden"; 

        popup.style.opacity = 0;
        popup.style.visibility = "hidden";

        abas_config_sobre.forEach(aba => {
            aba.classList.remove('active');
        });

    };
    radios.forEach(radio => {

        radio.addEventListener("click", function(){
            mudarCorGrafico(radio.value);
        });
    })
}

function mudarCorGrafico(cor){
    const grafTempo = Bokeh.documents[0].get_model_by_name("Tempo");
    const grafFreq = Bokeh.documents[1].get_model_by_name("Frequencia");

    if(document.getElementById("grafico_tempo").style.display !== "none" && grafTempo){

        corOposta = (cor === "black" ? "white" : (cor === "white" ? "black": console.log("Cor nao existente"))); 

        grafTempo.background_fill_color = cor;
        grafTempo.border_fill_color = cor;
        grafTempo.left[0].axis_label_text_color = corOposta;
        grafTempo.left[0].axis_line_color = corOposta; 
        grafTempo.left[0].major_label_text_color = corOposta; 
        grafTempo.below[0].axis_label_text_color = corOposta;
        grafTempo.below[0].major_label_text_color = corOposta;

        console.log("Grafico tempo ativo!");
    } else if (document.getElementById("grafico_frequencia").style.display !== "none" && grafFreq){
        grafFreq.background_fill_color = cor;
        grafFreq.border_fill_color = cor;
        console.log("Grafico frequencia ativado");
    }
}
// Inicializa o dom

document.addEventListener('DOMContentLoaded', function() {
    iniciarAbas();
    trocarAbas('tempo');
    startListeners();
    atualizarAPI();
});










