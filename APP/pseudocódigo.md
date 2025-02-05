PSEUDOCÓGIDO = GER_OND_APP 


FUNÇÕES A SEREM UTILIZADAS

FUNÇÃO gerar_sinal(tipo_sinal, amplitude, frequencia, duracao, offset):

    DEFINIR taxa_amostragem como valor adequado (por exemplo, 1000 Hz)
    CRIAR vetor_tempo de 0 até duracao com intervalos de 1/taxa_amostragem
    
    SE tipo_sinal for 'a'	SENOIDAL:
    SOLICITAR "Escreva a fase:" e LER fase
        sinal = amplitude * seno(2 * π * frequencia * vetor_tempo + fase) + offset
    SENÃO SE tipo_sinal for 'b': QUADRADO
        SOLICITAR "Escreva a fase:" e LER fase
        SOLICITAR "Escreva o duty cycle:" e LER duty
        sinal = amplitude * sinal_quadrado(2 * π * frequencia * vetor_tempo + fase, duty) + offset
    SENÃO SE tipo_sinal for 'c':  TRIANGULAR
        SOLICITAR "Escreva a fase:" e LER fase
        sinal = amplitude * sinal_triangular(2 * π * frequencia * vetor_tempo + fase) + offset
     SENÃO SE tipo_sinal for ‘d':  RUÍDO BRANCO
         sinal =  gerar_ruido_branco(tamanho=tamanho(vetor_tempo),amplitude=amplitude)  + offset 
    SENÃO:
        EXIBIR "Tipo de sinal inválido."
        RETORNAR nulo
    
    RETORNAR vetor_tempo, sinal

///SERÁ IMPLEMENTADO??

/* 
FUNÇÃO carregar_sinal(caminho_arquivo):

    TENTAR:
        ABRIR arquivo no caminho_arquivo
        LER dados do arquivo
        vetor_tempo = extrair vetor de tempo dos dados
        sinal = extrair sinal dos dados
        FECHAR arquivo
        RETORNAR vetor_tempo, sinal
    EXCETO:
        EXIBIR "Erro ao carregar o arquivo."
        RETORNAR nulo

*/

FUNÇÃO aplicar_operacoes_matematicas(series_ativas, operacoes):

    // series_ativas: Lista de séries temporais ativas
    // operacoes: Lista de operações matemáticas (+, -, *, /)
    
    SE número de séries ativas for menor que 2:
        EXIBIR "Pelo menos duas séries devem estar ativas para operações matemáticas."
        RETORNAR nulo
    
    serie_resultante = series_ativas[0]  // Inicia com a primeira série
    
    PARA cada operação em operacoes:
        SE operação for '+':
            serie_resultante = serie_resultante + series_ativas[indice_atual + 1]
        SENÃO SE operação for '-':
            serie_resultante = serie_resultante - series_ativas[indice_atual + 1]
        SENÃO SE operação for '*':
            serie_resultante = serie_resultante * series_ativas[indice_atual + 1]
        SENÃO SE operação for '/':
            serie_resultante = serie_resultante / series_ativas[indice_atual + 1]
    
    RETORNAR serie_resultante



FUNÇÃO plotar_sinal_no_tempo(vetor_tempo, sinal):

    CRIAR nova figura
    PLOTAR vetor_tempo no eixo x e sinal no eixo y
    CONFIGURAR título do gráfico como "Sinal no Domínio do Tempo"
    ROTULAR eixo x como "Tempo (s)"
    ROTULAR eixo y como "Amplitude"
    HABILITAR zoom e pan (usando ipympl ou outra biblioteca interativa
    EXIBIR gráfico


FUNÇÃO plotar_espectro_de_frequencia(frequencias, amplitudes):

    CRIAR nova figura
    PLOTAR frequencias no eixo x e amplitudes no eixo y
    CONFIGURAR título do gráfico como "Espectro de Frequência"
    ROTULAR eixo x como "Frequência (Hz)"
    ROTULAR eixo y como "Amplitude"
    HABILITAR zoom e pan (usando ipympl ou outra biblioteca interativa)
    EXIBIR gráfico



FUNÇÃO aplicar_fft(sinal):

    N = comprimento do sinal
    fft_resultado = FFT(sinal)
    frequencias = calcular_frequencias_correspondentes(N)
    amplitudes = módulo(fft_resultado) / N
    RETORNAR frequencias, amplitudes




FLUXO PRINCIPAL

INICIAR Programa de Análise de Sinais

EXIBIR "Bem-vindo ao Analisador de Sinais"

REPETIR até que o usuário decida sair:

    EXIBIR "Menu Principal:"
    EXIBIR "1. Gerar novo sinal"
    // EXIBIR "2. Carregar sinal existente"
    EXIBIR "3 Aplicar operações matemáticas entre séries ativas"
    EXIBIR "4. Aplicar Transformada Rápida de Fourier (FFT)"
    EXIBIR "5. Visualizar sinal no domínio do tempo"	BOX NO SITE
    EXIBIR "6. Visualizar espectro de frequência"	BOX NO SITE
    EXIBIR "7. Sair"
    SOLICITAR "Selecione uma opção (1-7):" e LER opção_do_usuario

    SE opção_do_usuario == 1:
        EXIBIR "Tipos de Sinais Disponíveis:"
        EXIBIR "a. Senoidal"
        EXIBIR "b. Quadrado"
        EXIBIR "c. Triangular”
        EXIBIR “d. Ruído Branco’’
        SOLICITAR "Selecione o tipo de sinal (a-d):" e LER tipo_sinal

        SOLICITAR "Digite a frequência do sinal (Hz):" e LER frequencia
        SOLICITAR "Digite a amplitude do sinal:" e LER amplitude
        SOLICITAR "Digite a duração do sinal (segundos):" e LER duracao

        CHAMAR função gerar_sinal(tipo_sinal, frequencia, amplitude, duracao)
        CHAMAR função plotar_sinal_no_tempo(sinal)
        // CHAMAR função plotar_espectro_de_frequencia(fft_resultado)

        EXIBIR "Sinal gerado com sucesso."

///SERÁ IMPLEMENTADO?
 
/*	
    SENÃO SE opção_do_usuario == 2:
        SOLICITAR "Digite o caminho do arquivo do sinal:" e LER caminho_arquivo
        CHAMAR função carregar_sinal(caminho_arquivo)
        EXIBIR "Sinal carregado com sucesso."
*/


    SENÃO SE opção_do_usuario == 3:
        SE sinal_está_disponível:
            CHAMAR função aplicar_fft(sinal)
            EXIBIR "FFT aplicada com sucesso."
        SENÃO:
            EXIBIR "Nenhum sinal disponível. Por favor, gere ou carregue um sinal primeiro."

    SENÃO SE opção_do_usuario == 4:
        SE sinal_está_disponível:
            CHAMAR função plotar_sinal_no_tempo(sinal)
        SENÃO:
            EXIBIR "Nenhum sinal disponível. Por favor, gere ou carregue um sinal primeiro."

    SENÃO SE opção_do_usuario == 5:
        SE fft_foi_aplicada:
            CHAMAR função plotar_espectro_de_frequencia(fft_resultado)
        SENÃO:
            EXIBIR "FFT não foi aplicada. Por favor, aplique a FFT primeiro."

    SENÃO SE opção_do_usuario == 6:
        EXIBIR "Saindo do programa. Até logo!"
        SAIR do loop

    SENÃO:
        EXIBIR "Opção inválida. Por favor, selecione uma opção válida."

FINALIZAR Programa de Análise de Sinais




