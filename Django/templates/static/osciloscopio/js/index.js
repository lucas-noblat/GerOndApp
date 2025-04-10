    function mostrarDivDuty() {
  
        const forma_sinal = document.getElementById('entrada-forma-sinal').value;
        const dutyDiv = document.getElementById('grupo-duty');

        if(forma_sinal === "quadrada" || forma_sinal === "triangular"){
            dutyDiv.style.display = "flex";
            dutyDiv.style.width = "50%";
        } else {
            dutyDiv.style.display = "none";
        }
   
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Chama a função uma vez ao carregar para configurar o estado inicial
        mostrarDivDuty();
        
        // Adiciona o event listener corretamente
        document.getElementById('entrada-forma-sinal').addEventListener('change', mostrarDivDuty);
    });