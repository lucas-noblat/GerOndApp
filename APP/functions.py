# Bibliotecas utilizadas


import numpy as np
import matplotlib.pyplot as plt

import scipy as scp
from ipywidgets import widgets, interact
from bokeh.plotting import figure, show

# Constantes utilizadas

largura_grafico = 400
altura_grafico = 400


# DEFINIÇÃO DA TAXA DE AMOSTRAGEM QUE SERÁ UTILIZADA EM NOSSO SISTEMA
taxaAmostragem = 1000 #Hz/s

'''FUNÇÕES DE VISUALIZAÇÃO (PLOTAGEM) '''

'''- Matplotlib'''


# FUNÇÃO PARA PLOTAR 1 SÉRIE EM GRÁFICO

def plotar(vetor_tempo, sinal, nome, largura=1280, altura=720, legenda=None, salvar_como=None):
    """
    Plota um sinal no domínio do tempo.

    Parâmetros:
    vetor_tempo: Vetor de tempo correspondente ao sinal.
    sinal: Sinal a ser plotado.
    nome: Título do gráfico.
    largura: Largura da figura em pixels (padrão: 1280).
    altura: Altura da figura em pixels (padrão: 720).
    legenda: Legenda do gráfico (opcional).
    salvar_como: Nome do arquivo para salvar o gráfico (opcional).
    """
    # Calcula o tamanho da figura em polegadas
    dpi = 100  # DPI padrão do Matplotlib
    largura_grafico = largura / dpi
    altura_grafico = altura / dpi

    # Configura a figura
    plt.figure(figsize=(largura_grafico, altura_grafico))
    plt.plot(vetor_tempo, sinal, label=legenda)
    plt.title(nome)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    # Adiciona a legenda, se fornecida
    if legenda is not None:
        plt.legend()

    # Salva a figura, se solicitado
    if salvar_como:
        plt.savefig(salvar_como, dpi=dpi)

    # Exibe o gráfico
    plt.show()


# FUNÇÃO PARA PLOTAR COM ORIGEM CENTRALIZADA

# FUNÇÃO PARA PLOTAR 1 SÉRIE EM GRÁFICO

def plotar_origem_centralizada(sinal, periodo, nome, largura=1280, altura = 720):

    # Define altura e largura do gráfico gerado

    largura_grafico = largura/100
    altura_grafico = altura/100
    
    # Criar e configurar gráfico
    plt.figure(figsize = (largura_grafico,altura_grafico))
    plt.plot(periodo,sinal)
    plt.title(nome)
    plt.xlabel('Tempo(s)')
    plt.ylabel('Amplitude')
    
    # Centralizar o zero no meio do gráfico
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # Linha horizontal no y=0
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')  # Linha vertical no x=0

    # Ajustar os limites dos eixos para centralizar o zero
    max_x = max(abs(periodo))  # Valor máximo absoluto de x
    max_y = max(abs(sinal))  # Valor máximo absoluto de y
    plt.xlim(-max_x, max_x)  # Limites simétricos no eixo x
    plt.ylim(-max_y, max_y)  # Limites simétricos no eixo y

    plt.grid()
    plt.show()
    
    
    

# FUNÇÃO PARA PLOTAR N SÉRIES COM SUAS RESPECTIVAS LEGENDAS EM UM SÓ GRÁFICO

def plotar_sinais(vetorTempo, titulo, *sinais, labels=None):

    plt.figure(figsize=(10,5))

    #Cria legendas aleatórias caso nenhuma for informada
    if labels is None:
        labels = [f"Sinal {i+1}" for i in range(len(sinais))] 

    #Plota cada sinal com sua respectiva legenda
    for i, sinal in enumerate(sinais):
        plt.plot(vetorTempo, sinal, label = labels[i])

    #Configura restante das infos
    plt.legend()
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.title(titulo)
    plt.grid()
    plt.show()


#FUNÇÃO PARA PLOTAR SÉRIES EM SEUS GRÁFICOS DE UMA SÓ VEZ
def subplotar(sinal, t, nome, qtd_sinais, posicao):
    plt.figure(figsize = (10,5))
    plt.subplot (qtd_sinais, 1, posicao)
    plt.plot(t, sinal, label = nome)
    plt.title(nome)
    plt.grid()

# FUNÇÃO PARA PLOTAR EM UMA GRID 2x2
def plotar_2x2(sinal1, sinal2, sinal3, sinal4, t, labels=None):
    # Cria legendas caso nenhuma for informada
    if labels is None:
        labels = [f"Sinal {i+1}" for i in range(4)]  # Corrigido para 4 sinais

    # Criar os subplots (2 linhas, 2 colunas)
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))

    # Adicionar os sinais aos subplots
    axs[0, 0].plot(t, sinal1, label=labels[0], color = 'blue')
    axs[0, 0].set_title(labels[0])

    axs[0, 1].plot(t, sinal2, label=labels[1], color = 'yellow')
    axs[0, 1].set_title(labels[1])
    
    axs[1, 0].plot(t, sinal3, label=labels[2], color = 'green')
    axs[1, 0].set_title(labels[2])

    axs[1, 1].plot(t, sinal4, label=labels[3], color = 'red')
    axs[1, 1].set_title(labels[3])

    # Melhorar a apresentação dos gráficos
    for ax in axs.flat:
        ax.set_xlabel("Tempo (s)")
        ax.set_ylabel("Amplitude")
        ax.grid(True)

    plt.tight_layout()
    plt.show()

'''Bokeh'''


''' FUNÇÕES PARA CRIAR OS SINAIS '''

import numpy as np

# Onda Senoidal

def sinal_senoidal(amplitude, frequencia, taxa_amostragem=100, duracao=1, fase=0, offset=0):
    """
    Gera um sinal senoidal.

    Parâmetros:
    amplitude: Amplitude do sinal.
    frequencia: Frequência do sinal em Hz.
    taxa_amostragem: Taxa de amostragem em amostras por segundo (default é 1).
    duracao: Duração do sinal em segundos (default é 1).
    fase: Fase inicial do sinal em radianos (default é 0).
    offset: Deslocamento vertical do sinal (default é 0).

    Retorna:
    vetor_tempo: Vetor de tempo correspondente ao sinal.
    s: Sinal senoidal gerado.
    """
    if taxa_amostragem <= 0:
        raise ValueError("A taxa de amostragem deve ser maior que zero.")
    if duracao <= 0:
        raise ValueError("A duração deve ser maior que zero.")

    # Definindo o vetor tempo
    vetor_tempo = np.linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False)

    # Sinal gerado
    s = amplitude * np.sin(2 * np.pi * frequencia * vetor_tempo + fase) + offset

    # Retornando
    return vetor_tempo, s

# ONDA TRIANGULAR
def sinal_triangular(amplitude, frequencia, taxa_amostragem = 1, duracao = 1, fase = 0, offset = 0, duty=0):
    
    # Definindo o delta_t
    intervalo_amostragem = 1/taxa_amostragem

    # Gerando o vetor tempo para ser o eixo x

    t = np.arrange(0, duracao, intervalo_amostragem)


    return (amplitude * scp.signal.sawtooth (2*np.pi*frequencia*t, duty) + offset)

# ONDA QUADRADA
def sinal_quadrada(amplitude, frequencia, t, duty):
    return amplitude * scp.signal.square(2*np.pi*frequencia*t, duty = duty)

# RUÍDO BRANCO
def ruido_branco(amplitude, duracao, taxa_amostragem = 1000):

    #Número de amostras
    num_amostras = int(duracao * taxa_amostragem)

    #Criando o ruído
    ruido_branco = np.random.normal(0, amplitude, num_amostras)

    return ruido_branco


#FUNÇÃO PARA GERAR SINAIS

def gerar_sinal(tipo_sinal, amplitude, frequencia, duracao, offset):

    # Calcula o número de pontos
    num_pontos = int(duracao * taxaAmostragem)

    vetor_tempo = np.linspace(0, duracao, num_pontos, endpoint = False) #Vetor para criar as séries
    sinal_criado = None

    #SENOIDAL
    if tipo_sinal == 'a': 
        fase = float(input('Digite a fase da onda'))
        sinal_criado = amplitude * np.sin(2*np.pi*frequencia*vetor_tempo + fase) + offset
    elif tipo_sinal == 'b':
        fase = float(input('Digite a fase da onda'))
        duty = float(input('Digite o duty cycle'))
        sinal_criado = amplitude * scp.signal.square(2*np.pi*frequencia*vetor_tempo, duty = duty)
    else:
        print('Sinal inválido')
    return sinal_criado


''' FUNÇÃO PARA APLICAR AS OPERAÇÕES ENTRE AS SÉRIES ATIVAS '''

def aplicar_operacoes(series_ativas, operacoes):
    # Verifica se existem pelo menos duas séries ativas
    if len(series_ativas) < 2:
        print('Pelo menos duas séries precisam estar ativas para efetuar as operações')
        return None
    # Verifica se o número de operações é compatível com o número de séries

    if len(operacoes) != len(series_ativas) - 1:
        print('O número de operações deve ser exatamente 1 a menos do que o número de séries ativas')
        return None
        
    serie_resultante = series_ativas[0].copy()

    # Aqui vai uma curiosidade insana que em meio a codificação acabei deixando passar:
    
    # LEMBRAR SEMPRE QUE QUANDO ATRIBUIR UM OBJETO (UM PONTEIRO DO OBJETO) A UMA VARIÁVEL EM PYTHON (UM OBJETO,)
    # QUALQUER ALTERAÇÃO NA VARIÁVEL ATRIBUÍDA IRÁ ALTERAR O OBJETO 'APONTADO', POR ISSO USAMOS UMA CÓPIA DA INSTÂNCIA

    
    for i, operacao in enumerate(operacoes):
        if operacao == '+':
            serie_resultante += series_ativas[i+1]
        elif operacao == '-':
            serie_resultante -= series_ativas[i+1]
        elif operacao == '*':
            serie_resultante *= series_ativas[i+1]
        elif operacao == '/':
            serie_resultante /= series_ativas[i+1]
        else:
            print(f'Operação "{operacao}" inválida.  Use apenas "+", "-", "*" ou "/".')
            return None
    return serie_resultante
