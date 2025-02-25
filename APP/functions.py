# Bibliotecas utilizadas


import numpy as np
import matplotlib.pyplot as plt

import scipy as scp
from ipywidgets import widgets, interact
from bokeh.plotting import figure, show
from scipy.signal import square

# DEFINIÇÃO DA TAXA DE AMOSTRAGEM QUE SERÁ UTILIZADA EM NOSSO SISTEMA
taxaAmostragem = 1000 #Hz/s

'''FUNÇÕES DE VISUALIZAÇÃO (PLOTAGEM) '''

'''- Matplotlib(Apenas para criação de notebooks)'''


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


'''Bokeh'''


''' FUNÇÕES PARA CRIAR OS SINAIS '''

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
def sinal_triangular(amplitude, frequencia, taxa_amostragem = 1000, duracao = 1, fase = 0, offset = 0, duty=0):
    
    """
    Gera um sinal triangular.

    Parâmetros:
    amplitude: Amplitude do sinal.
    frequencia: Frequência do sinal em Hz.
    taxa_amostragem: Taxa de amostragem em amostras por segundo (default é 1).
    duracao: Duração do sinal em segundos (default é 1).
    fase: Fase inicial do sinal em radianos (default é 0).
    offset: Deslocamento vertical do sinal (default é 0).

    Retorna:
    vetor_tempo: Vetor de tempo correspondente ao sinal.
    triangular
    : Sinal triangular gerado.
    """


    # Gerando o vetor tempo para ser o eixo x

    vetor_tempo = np.linspace(0, duracao, int(duracao*taxa_amostragem))
    triangular = (amplitude * scp.signal.sawtooth (2*np.pi*frequencia*vetor_tempo + fase, duty) + offset)

    return vetor_tempo, triangular


# ONDA QUADRADA 
def sinal_quadrado(amplitude, frequencia, taxa_amostragem=1000, duracao=1, fase=0, offset=0, duty=0.5):
    """
    Gera um sinal quadrado usando a função square do scipy.signal.

    Parâmetros:
    amplitude: Amplitude do sinal.
    frequencia: Frequência do sinal em Hz.
    taxa_amostragem: Taxa de amostragem em amostras por segundo (default é 1000).
    duracao: Duração do sinal em segundos (default é 1).
    fase: Fase inicial do sinal em radianos (default é 0).
    offset: Deslocamento vertical do sinal (default é 0).
    duty: Ciclo de trabalho do sinal quadrado (default é 0.5, ou 50%).

    Retorna:
    vetor_tempo: Vetor de tempo correspondente ao sinal.
    sinal_quadrado: Sinal quadrado gerado.
    """
    # Verifica se os parâmetros são válidos
    if taxa_amostragem <= 0:
        raise ValueError("A taxa de amostragem deve ser maior que zero.")
    if duracao <= 0:
        raise ValueError("A duração deve ser maior que zero.")
    if duty <= 0 or duty >= 1:
        raise ValueError("O ciclo de trabalho (duty) deve estar entre 0 e 1.")

    # Define o vetor de tempo
    vetor_tempo = np.linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False)

    # Gera o sinal quadrado usando scipy.signal.square
    sinal_quadrado = amplitude * square(2 * np.pi * frequencia * vetor_tempo + fase, duty=duty) + offset

    return vetor_tempo, sinal_quadrado


# RUÍDO BRANCO
def ruido_branco(amplitude, num_componentes, duracao=1, offset=0, freq_inicial=0, freq_final=0,):
    """
    Gera um ruído branco com os parâmetros especificados.

    Parâmetros:
    amplitude: Amplitude do ruído (unidade especificada pelo usuário).
    freq_inicial: Frequência inicial (Hz).
    freq_final: Frequência final (Hz).
    num_componentes: Número de componentes (amostras) no ruído.
    duracao: Duração do ruído em segundos.
    offset: Deslocamento vertical do ruído (mesma unidade da amplitude).

    Retorna:
    vetor_tempo: Vetor de tempo correspondente ao ruído.
    ruido: Sinal de ruído branco gerado.
    """
    # Verifica se os parâmetros são válidos
    if freq_inicial < 0 or freq_final < 0:
        raise ValueError("As frequências devem ser maiores ou iguais a zero.")
    if num_componentes <= 0:
        raise ValueError("O número de componentes deve ser maior que zero.")
    if duracao <= 0:
        raise ValueError("A duração deve ser maior que zero.")

    # Gera o vetor de tempo
    vetor_tempo = np.linspace(0, duracao, num_componentes, endpoint=False)

    # Gera o ruído branco
    ruido = amplitude * np.random.normal(0, 1, num_componentes) + offset

    return vetor_tempo, ruido


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
