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

        abaAtiva.style.border = coresAbas[sinal] || "2px solid blue";
    }
    
    // Atualiza o html com as entradas do sinal clicado

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
        dutyDiv.style.width = "50%";
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


// Inicializa o dom
document.addEventListener('DOMContentLoaded', function() {
    iniciarAbas();
});

document.addEventListener('DOMContentLoaded', function() {
trocarAbas('tempo');
});
