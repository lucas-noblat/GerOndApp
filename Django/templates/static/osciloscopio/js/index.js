// BOOLEANOS QUE AJUDARAM A AJUSTAR PERﾃ弘DO <--> FREQUENCIA

let atualizandoFrequencia = false;
let atualizandoPeriodo = false;


// CONTROLE DAS ABAS - VERSﾃグ DEFINITIVA
function iniciarAbas() {
    // Ativa a aba inicial
    const sinalInicial = document.getElementById('numero_sinal').value;
    ativarAba(sinalInicial);
    
    // Configura eventos dos botﾃｵes
    document.querySelectorAll('.botao-sinal').forEach(btn => {
        btn.addEventListener('click', function() {
            const sinal = this.getAttribute('data-sinal');
            ativarAba(sinal);
            carregarParametrosSinal(sinal);

        });
    });
    
    // Controle do duty cycle
    document.getElementById('entrada-forma-sinal').addEventListener('change', mostrarDivDuty);
    mostrarDivDuty(); // Configura estado inicial


}


// ATIVAR AS ABAS
function ativarAba(sinal) {

    // Atualiza informacoes no front
    carregarParametrosSinal(sinal);

    // Pega a div das entradas para destacar

    const formEntrada = document.getElementById("form-entrada");
    const containerEntradas = document.getElementById("container-entradas");

    // Remove classe active de todas as abas
    document.querySelectorAll('.botao-sinal').forEach(aba => {
        aba.classList.remove('active');
        aba.style.border = "";
    });
    
    // Ativa a aba clicada (botﾃ｣o)
    const abaAtiva = document.querySelector(`.botao-sinal[data-sinal="${sinal}"]`);
    if (abaAtiva && formEntrada) {

        abaAtiva.classList.add('active');        
        const coresAbas = {
            1: "3px solid blue",
            2: "3px solid orange",
            3: "3px solid green",
            4: "3px solid red",
            5: "3px solid purple"
        }

        const coresFundoAbas = {
            1: "#E0F2FE",
            2: "#FFF7ED",
            3: "#F0FDF4",
            4: "#FEF2F2",
            5: "#FAF5FF"
        }

        const coresFundoContainer = {
            1: "#7fbfff",
            2: "#ffd299",
            3: "#66cc66",
            4: "#ff8080",
            5: "#b380b3"
        }

        // Define a cor da aba dependendo do sinal, por padrﾃ｣o ﾃｩ azul
        abaAtiva.style.border = coresAbas[sinal] || "3px solid blue";
        formEntrada.style.border = coresAbas[sinal] || "3px solid blue";
        formEntrada.style.backgroundColor = coresFundoAbas[sinal] || "#E0F2FE"; 
        containerEntradas.style.backgroundColor = coresFundoContainer[sinal] || "#7fbfff";

        // Atualiza a URL sem recarregar a pﾃ｡gina
        const url = new URL(window.location);
        url.searchParams.set('sinal', sinal);
        window.history.pushState({}, '', url);
    }
    
    // Atualiza campo hidden
    document.getElementById('numero_sinal').value = sinal;
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
    aba_ativa ? aba_ativa.classList.add('active') : window.alert('Essa aba nﾃ｣o existe');

    if(aba_clicada !== "ambos"){   
        const grafico_ativo = document.querySelector(`.grafico#grafico_${aba_clicada}`);
    
       
        
        grafico_ativo ? grafico_ativo.style.display = 'flex' : window.alert('Esse grﾃ｡fico nﾃ｣o existe');
        grafico_ativo ? grafico_ativo.style.height = '100%' : window.alert("Esse grﾃ｡fico nﾃ｣o existe");
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

    setTimeout(atualizarRanges, 50);

}




// Funﾃｧﾃ｣o para receber dados (BACKEND -> FRONTEND)


// Vari疱el para descobrir protocolo e host para usar na api

const BASE_URL = `${window.location.protocol}//${window.location.host}`;

async function getData(sinal){

        try{
            const response = await fetch(`${BASE_URL}/api/getData/?sinal=${sinal}`);

            if(!response.ok){
                throw new Error ("Nﾃ｣o foi possﾃｭvel carregar a API");
            }

            return response.json();
     
        } catch(error){
            console.error(error);
        }

}

// Funﾃｧﾃ｣o para enviar dados (FRONTEND -> BACKEND)

async function sendData(sinal){

        const parametros = receberParametros();


        try{
            const response = await fetch(`${BASE_URL}/api/sendData/?sinal=${sinal}`, {
                method: 'POST',
                headers: { 'Content-Type' : 'application/json'},
                body: JSON.stringify(parametros)
            })

            if(!response.ok){
                throw new Error("Nﾃ｣o foi possﾃｭvel resgatar api");}

            return await response.json();
        } catch(error){
            throw error;
        }
 
}

async function carregarParametrosSinal(sinal){
    try{
        const dados = await getData(sinal);
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
        document.getElementById("entrada-duty").value = dados['duty'];
        document.getElementById("entrada-periodo").value = parseFloat(1/dados['frequencia']);
        document.getElementById("entrada-duracao").value = dados['duracao'];
        document.getElementById("entrada-rate").value = dados['rate'];

    }
    catch(error){
        console.error(error);
    }
}

// RECEBE OS DADOS DO PARﾃ�ETRO

function receberParametros(){
    

    const sinal = document.getElementById('numero_sinal').value;
    const operacoes = [
        document.getElementById("entrada-operacao-0").value,
        document.getElementById(`entrada-operacao-1`).value,
        document.getElementById(`entrada-operacao-2`).value,
        document.getElementById(`entrada-operacao-3`).value,
        document.getElementById(`entrada-operacao-4`).value,
    ];

    const parametros = {
        id: sinal,
        amplitude: parseFloat(document.getElementById("entrada-amplitude").value),
        rate: parseFloat(document.getElementById("entrada-rate").value),
        frequencia: parseFloat(document.getElementById("entrada-frequencia").value),
        duracao: parseFloat(document.getElementById("entrada-duracao").value),
        fase: parseFloat(document.getElementById("entrada-fase").value) * (Math.PI/180.0),
        offset: parseFloat(document.getElementById("entrada-offset").value),
        operacao: operacoes,
        duty: parseFloat(document.getElementById("entrada-duty").value) || 0.5,
        forma_sinal: document.getElementById("entrada-forma-sinal").value,
        }

    return parametros;
}

function receberUnidades(){ 
    return {
        amplitude: document.getElementById("unidade-amplitude").value,
        tempo: document.getElementById("unidade-duracao").value,
        frequencia: document.getElementById("unidade-frequencia").value,
    };
}


// Funﾃｧﾃ｣o assﾃｭncrona que irﾃ｡ atualizar os dados

async function atualizarAPI(){

    const sinal =document.getElementById('numero_sinal').value || "1";


    try{

        // Atualizando as unidades

        const resultadoSendData = await sendData(sinal);

        for(let i = 0; i < 6; i++){
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
                
            }else {
                console.warn("Nﾃ｣o foi possﾃｭvel atualizar o grﾃ｡fico: dados ou source nﾃ｣o definidos.");
            }
            
        }
        atualizarRanges();
    } catch(error){
        console.error(error);
    }

}


// FUNﾃ�グ QUE ATUALIZA UNIDADES

function atualizarUnidades(){

    const unidades = receberUnidades();

    const grafTempo = Bokeh.documents[0].get_model_by_name("Tempo");
    const grafFreq = Bokeh.documents[1].get_model_by_name("Frequencia");

    if(grafFreq && grafTempo) {
        grafTempo.left[0].axis_label = `Amplitude(${unidades['amplitude']})`;
        grafTempo.below[0].axis_label = `Tempo(${unidades['tempo']})`;

        grafFreq.left[0].axis_label = `Magnitude(${unidades['amplitude']})`;
        grafFreq.below[0].axis_label = `Frequencia(${unidades['frequencia']})`;

    }
    else {
        console.warning("Grﾃ｡ficos nﾃ｣o encontrados");
    }




}

// FUNﾃ�グ PARA ATUALIZAR OS STES DOS INPUTS

function atualizarSteps(){

    document.querySelectorAll('input[type = "number"').forEach(input => {

        // Atualizaﾃｧﾃ｣o do step dos inputs (Pedido do Fﾃ｡bio)

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
// FUNﾃ�グ PARA ESCONDER OS SINAIS INICIALMENTE

function inicializarSinais() {

    // Grﾃ｡ficos

    const grafTempo = Bokeh.documents[0].get_model_by_name("Tempo");
    const grafFreq = Bokeh.documents[1].get_model_by_name("Frequencia");

    // SINCRONIZAR A FERRAMENTA RESET COM NOSSA ATUALIZARRANGES()

    grafTempo.on_event("reset", function(){
        setTimeout(atualizarRanges, 50);
    });
    grafFreq.on_event("reset", function(){
        setTimeout(atualizarRanges, 50);
    });


    // LOOP PARA ESCONDER SINAIS NO FRONT

    for (let i = 0; i < 6; i++) {
        const linhaTempo = Bokeh.documents[0].get_model_by_name(`linha${i}`);
        const linhaFreq = Bokeh.documents[1].get_model_by_name(`linha${i}`);

        if (linhaTempo && linhaFreq) {
            // Apenas o primeiro sinal fica visﾃｭvel
            if (i === 0) {
                linhaTempo.visible = true;
                linhaFreq.visible = true;
            } else {
                linhaTempo.visible = false;
                linhaFreq.visible = false;
            }
        }
    }
    setTimeout(atualizarRanges, 50);
}

// FUNﾃ�グ PARA AJUSTAR A DIMENSﾃグ DO GRﾃ：ICO CONFORME SINAIS VISﾃ昂EIS

function atualizarRanges() {
  
    // Ajustar grﾃ｡fico de tempo
    const docTempo = Bokeh.documents[0];
    const plotTempo = docTempo.get_model_by_name("Tempo");

    // Ajustar grﾃ｡fico de frequﾃｪncia
    const docFreq = Bokeh.documents[1];
    const plotFreq = docFreq.get_model_by_name("Frequencia");

    let xs = [], ys = [];
    let xFreqs = [], yFreqs = [];

    // Loop em todos os sinais
    for (let i = 0; i < 6; i++) {
        const linhaTempo = docTempo.get_model_by_name(`linha${i}`);
        const linhaFreq = docFreq.get_model_by_name(`linha${i}`);

        if (linhaTempo && linhaTempo.visible) {
        xs = xs.concat(linhaTempo.data_source.data['x']);
        ys = ys.concat(linhaTempo.data_source.data['y']);
        }

        if (linhaFreq && linhaFreq.visible) {
        xFreqs = xFreqs.concat(linhaFreq.data_source.data['x']);
        yFreqs = yFreqs.concat(linhaFreq.data_source.data['y']);
        }
    }

    // Calcula min/max
    let max_X = Math.max(...xs), min_X = Math.min(...xs);
    let max_Y = Math.max(...ys), min_Y = Math.min(...ys);
    let max_X_frequencia = Math.max(...xFreqs), min_X_frequencia = Math.min(...xFreqs);
    let max_Y_frequencia = Math.max(...yFreqs), min_Y_frequencia = Math.min(...yFreqs);

    // 隼 Corrigir caso todos os valores sejam iguais
    if (max_X === min_X) { max_X += 1; min_X -= 1; }
    if (max_Y === min_Y) { max_Y += 1; min_Y -= 1; }
    if (max_X_frequencia === min_X_frequencia) { max_X_frequencia += 1; min_X_frequencia -= 1; }
    if (max_Y_frequencia === min_Y_frequencia) { max_Y_frequencia += 1; min_Y_frequencia -= 1; }


    const xPadding = (max_X - min_X) * 0.1; 
    const yPadding = (max_Y - min_Y) * 0.1;

    const xPaddingFreq = (max_X_frequencia - min_X_frequencia) * 0.1; 
    const yPaddingFreq = (max_Y_frequencia - min_Y_frequencia) * 0.1;

    // Atualizar ranges do tempo
    if (xs.length > 0 && ys.length > 0) {
        plotTempo.x_range.start = min_X - xPadding;
        plotTempo.x_range.end = max_X + xPadding;
        plotTempo.y_range.start = min_Y - yPadding;
        plotTempo.y_range.end = max_Y + yPadding;
    }

    // Atualizar ranges da frequﾃｪncia
    if (xFreqs.length > 0 && yFreqs.length > 0) {
        plotFreq.x_range.start = min_X_frequencia - xPaddingFreq;
        plotFreq.x_range.end = max_X_frequencia + xPaddingFreq;
        plotFreq.y_range.start = min_Y_frequencia - yPaddingFreq;
        plotFreq.y_range.end = max_Y_frequencia + yPaddingFreq;
    }

        plotTempo.change.emit();
        plotFreq.change.emit();

}

// INCREMENTO / DECREMENTO ATRAVﾃ唄 DO BOTﾃグ
 let cursorPosicao = {}

function incrementaInput(input){
    
    const entrada = document.getElementById(`entrada-${input}`);
    if(!entrada) return; //Defesa
    
    // PARA O STEP
    
    //valor = Number(entrada.value);

    //const step = Number(document.getElementById("entrada-step").value);
    //entrada.step = step;

    //valor += step;
    //if(valor < 0) valor = 0;

    entrada.stepUp();

    if(input == "frequencia") atualizaPeriodo();
    if(input == "periodo") atualizaFreq();

    atualizarAPI();
}


function decrementaInput(input){

    const entrada = document.getElementById(`entrada-${input}`);
    if(!entrada) return;
    entrada.stepDown();
    
    // PARA O STEP
    //valor = Number(entrada.value);

    //const step = Number(document.getElementById("entrada-step").value);
    //entrada.step = step;
    //valor -= step;
    //if(valor < 0) valor = 0;
    //entrada.value = valor;
    
    
    if(input == "frequencia") atualizaPeriodo();
    if(input == "periodo") atualizaFreq();
    atualizarAPI();
}



// FUNﾃ�グ PARA ATIVAR OS LISTENERS

function startListeners() {
    const inputs = document.querySelectorAll('input[type="number"]');
    const selects = document.querySelectorAll("select");
    const radios = document.querySelectorAll('input[type="radio"]');

    // POPUP
    let popup = null;

    const abas_config_sobre = document.querySelectorAll(".container-aba");

    const overLayerPopup = document.getElementById("blur-popup");
    const fechar_popup = document.querySelectorAll(".fechar-popup");



    // TODOS OS INPUTS NUMﾃ嘘ICOS
    inputs.forEach(input => {
        input.addEventListener("input", async function() {
            await atualizarAPI()
            atualizarUnidades();
            atualizarRanges();
        })     
    });
    

    // TODOS OS INPUT DO TIPO SELECT
    selects.forEach(select => {
        select.addEventListener("change", function(){

            if(this.id != "select-tamanho"){ //SELECIONA TODOS MENOS O DO TAMANHO DA JANELA DO POPUP
                atualizarUnidades();
                atualizarAPI();

            } else { // SE FOR O SELECT DA MUDANﾃ② DE TELA MUDA O TAMANHO DA TELA

                const janela = document.getElementById("janela-principal");
                if(janela) {
                    switch(this.value){
                        case "pequeno":
                            janela.style.width = "960px";
                            janela.style.height = "540px";
                            break;    
                        case "medio":
                            janela.style.width = "1280px";
                            janela.style.height = "720px";
                            break;                     
                         case "grande":
                            janela.style.width = "1600px";
                            janela.style.height = "900px";
                            break; 
                         case "enorme":
                            janela.style.width = "1920px";
                            janela.style.height = "1080px";
                            break;                    
                        default:
                            console.error("Tamanho inexistente");
                    }
                }
                

            }
        });
        if(select.name == "entrada-operacao") {
            select.addEventListener("click", function(){
                let num = Number(this.getAttribute("data-indice")) + 1;
                ativarAba(num);
            });    
        };
        
    });

    // SINAIS VISﾃ昂EIS

    sinais.forEach((sinal, i) => {


        // QUANDO MUDA
        sinal.addEventListener("change", function(){
            const linhaTempo = Bokeh.documents[0].get_model_by_name(`linha${i}`);
            const linhaFreq = Bokeh.documents[1].get_model_by_name(`linha${i}`);

            if(linhaFreq && linhaTempo) {
                const ativo = this.checked;
                linhaTempo.visible = ativo;
                linhaFreq.visible = ativo;
                setTimeout(atualizarRanges, 50);
            }
        })
    })

    // EVENTOS ABA DA ESQUERDA

    abas_config_sobre.forEach(aba => {
        aba.addEventListener("click", function(){
            if(aba.id == "configuracoes"){
                popup = document.getElementById("popup-config");
            } else if (aba.id == "sobre"){
                popup = document.getElementById("popup-sobre");

            }
            posicionarPopup(aba, popup);

            overLayerPopup.style.transition = "all 0.4 ease";
    
            overLayerPopup.style.opacity = 0.6;
            overLayerPopup.style.visibility = "visible";
            aba.classList.add('active');
    
        });
    });
    // ABA DE CONFIGURAﾃ�髭S

    fechar_popup.forEach(fechar => {
        fechar.onclick = function () {
            overLayerPopup.style.opacity = 0;
            overLayerPopup.style.visibility = "hidden";
    
            popup.style.opacity = 0;
            popup.style.visibility = "hidden";
    
            abas_config_sobre.forEach(aba => {
                aba.classList.remove('active');
            });
        };
    });

    radios.forEach(radio => {

        radio.addEventListener("click", function(){
            mudarCorGrafico(radio.value);
        });
    })

    // ATUALIZANDO FREQUENCIA E PERﾃ弘DO

    inputFrequencia.addEventListener("input", atualizaPeriodo);

    inputPeriodo.addEventListener("input", atualizaFreq);
}



// Variﾃ｡veis globais para ambais as funcs (a de cima e a de baixo)

const inputPeriodo = document.getElementById("entrada-periodo");
const inputFrequencia = document.getElementById("entrada-frequencia");


// FUNCOES PARA ATUALIZAR PERIODO <--> FREQUENCIA CONFORME UM DOS DOIS FOREM ALTERADOS
function atualizaPeriodo(){
        if(atualizandoPeriodo) return; //SE ATUALIZANDO PERIODO NAO FAZ NADA
        const f = parseFloat(inputFrequencia.value);
        if(!isNaN(f) && f > 0.000001){
            atualizandoFrequencia = true;
            const p = 1 / f; //periodo = 1/frequencia
            inputPeriodo.value = p.toFixed(4);
            atualizandoFrequencia = false;
        }
        setTimeout(atualizarAPI, 50);
    }


function atualizaFreq(){
    if(atualizandoFrequencia) return; //SE ATUALIZANDO PERIODO NAO FAZ NADA
    const p = parseFloat(inputPeriodo.value);
    if(!isNaN(p) && p > 0.000001){
        atualizandoPeriodo = true;
        const f = 1 / p;    //periodo = 1/frequencia
        inputFrequencia.value = f.toFixed(4);
        atualizandoPeriodo = false;
        
    }
    setTimeout(atualizarAPI, 50);
}




// POSICIONANDO POPUP AO LADO DE ABA CLICADA

function posicionarPopup(aba, popup){

    const retangulo = aba.getBoundingClientRect();

    const posX = retangulo.right + 10;
    const posY = retangulo.top;

    popup.style.left = `${posX}px`;
    popup.style.top = `${posY}px`;

    popup.style.opacity = 1;
    popup.style.visibility = "visible";

}






// FUNﾃ�グ DE MUDAR DE COR (INCOMPLETA)
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
        grafTempo.below[0].axis_line_color = corOposta;

    } else if (document.getElementById("grafico_frequencia").style.display !== "none" && grafFreq){
        grafFreq.background_fill_color = cor;
        grafFreq.border_fill_color = cor;
    }
}




// DICAS INICIAIS

function dicasIniciais(){

    // POPUP DICAS
    const dicaTamanho = document.getElementById("dica-tamanho");
    const dicaManual = document.getElementById("dica-manual");

    const overlay = document.querySelector(".popup-overlay");

    // ABAS/DICAS DA VEZ
    let aba;
    let dica;

    if(ehMobile()){
        // ESCONDE POPUP DE REDIMENSIONAMENTO E MOSTRA O DO MANUAL

        dicaTamanho.style.display = "none";
        dicaManual.style.display = "flex";
        aba = document.getElementById("sobre");
        dica = dicaManual;

    }

    else {
        aba = document.getElementById("configuracoes");
        dica = dicaTamanho;
    }
    
     // Primeira dica (tamanho) - destaca CONFIG
    overlay.style.display = "flex";

    // DEFINE QUAL ABA SERA DESTACADA (EM MOBILE SOMENTE A DO MANUAL POR ENQUANTO)


    posicionarPopup(aba, dica);
    criarDestaqueFlutuante(aba, "#28a745");

    // Configurar botﾃ｣o OK da primeira dica
    document.getElementById("btn-ok-1").onclick = function() {
        // Remove destaque da configuraﾃｧﾃ｣o
        removerDestaqueFlutuante();
        overlay.style.display = "none";
        // Mostra segunda dica (manual) - destaca SOBRE
        dicaTamanho.style.display = "none";
        dicaManual.style.display = "flex";
        posicionarPopup(document.getElementById("sobre"), dicaManual);
        criarDestaqueFlutuante(document.getElementById("sobre"), "#28a745");

        
        overlay.style.display = "flex"
        // Destacar a aba sobre
        if(abaSobre) abaSobre.classList.add('destaque-onboarding');
    };
    // Configurar botﾃ｣o OK da segunda dica
    document.getElementById("btn-ok-2").onclick = function() {
        // Remove destaque e fecha tudo
        removerDestaqueFlutuante();
        overlay.style.display = "none";
        dicaManual.style.display = "none";
        dicaTamanho.style.display = "block"; // Restaura para prﾃｳxima vez
    };
}




// FUNﾃ�グ PRA CLONAR DIV EM DESTAQUE


function criarDestaqueFlutuante(elementoAlvo, cor = "#007bff") {
    // Remove destaque anterior
    removerDestaqueFlutuante();
    
    // Obtﾃｩm a posiﾃｧﾃ｣o do elemento alvo
    const rect = elementoAlvo.getBoundingClientRect();
    
    // Cria div flutuante
    const destaque = document.createElement('div');
    destaque.innerHTML = elementoAlvo.innerHTML;
    destaque.className = 'destaque-flutuante';
    destaque.id = 'destaque-atual';
    destaque.style.cssText = `
        position: fixed;
        z-index: 10002;
        left: ${rect.left}px;
        top: ${rect.top}px;
        width: ${rect.width}px;
        height: ${rect.height}px;
        border: 1px solid ${cor};
        background-color: #C1C1C1;
        border-radius: 8px;
        box-shadow: 0 0 20px ${cor}80;
        pointer-events: none;
    `;
    
    document.body.appendChild(destaque);
    return destaque;
}

function removerDestaqueFlutuante() {
    const destaque = document.getElementById('destaque-atual');
    if (destaque) {
        destaque.remove();
    }
}


function ehMobile(){
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Inicializa o dom

document.addEventListener('DOMContentLoaded', async function() {

    dicasIniciais();
    iniciarAbas();
    trocarAbas('tempo');
    startListeners();

    // ESPERA DADOS SEREM TRAZIDOS DO BACKEND PARA ESCONDER E ATUALIZAR GRﾃ：ICO
    await atualizarAPI();
    inicializarSinais();
 
});



