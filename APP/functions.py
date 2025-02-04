import numpy as np
import matplotlib.pyplot as plt
import scipy as scp
from ipywidgets import widgets, interact

# DEFINIÇÃO DA TAXA DE AMOSTRAGEM QUE SERÁ UTILIZADA EM NOSSO SISTEMA
taxaAmostragem = 1000 #Hz/s

'''FUNÇÕES DE VISUALIZAÇÃO (PLOTAGEM) '''

# FUNÇÃO PARA PLOTAR 1 SÉRIE EM GRÁFICO

def plotar(sinal, periodo, nome):
    plt.figure(figsize = (10,3))
    plt.plot(periodo,sinal)
    plt.title(nome)
    plt.xlabel('Tempo(s)')
    plt.ylabel('Amplitude')
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


''' FUNÇÕES PARA CRIAR OS SINAIS '''

# ONDA SENOIDAL
def onda_senoidal(amplitude, frequencia, t, fase):
    return amplitude * np.sin(2*np.pi*frequencia*t + fase)

# ONDA TRIANGULAR
def onda_triangular(amplitude, frequencia, t, simetria):
    return amplitude * scp.signal.sawtooth (2*np.pi*frequencia*t, simetria)

# ONDA QUADRADA
def onda_quadrada(amplitude, frequencia, t, duty):
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

    vetor_tempo = np.linspace(0, duracao, num_pontos, endpoint = false) #Vetor para criar as séries
    sinal_criado = None

    #SENOIDAL
    if tipo_sinal == 'a': 
        fase = float(input('Digite a fase da onda'))
        sinal_criado = amplitude * np.sin(2*np.pi*frequencia*vetor_tempo + fase) + offset
    elif tipo_sinal == 'b':
        fase = float(input('Digite a fase da onda'))
        duty = float(input('Digite o duty cycle'))
        sinal_criado = amplitude * scp.signal.square(2*np.pi*frequencia*t, duty = duty)
    else:
        print('Sinal inválido')
    return sinal_criado

# Função para capturar entradas do usuário usando ipywidgets
def interface_gerar_sinal():
    tipo_sinal = widgets.Dropdown(options=['a', 'b'], description='Tipo de sinal:')
    amplitude = widgets.FloatText(value=1.0, description='Amplitude:')
    frequencia = widgets.FloatText(value=5.0, description='Frequência (Hz):')
    duracao = widgets.FloatText(value=2.0, description='Duração (s):')
    offset = widgets.FloatText(value=0.5, description='Offset:')
    taxaAmostragem = widgets.FloatText(value=1000.0, description='Taxa de amostragem (Hz):')
    fase = widgets.FloatText(value=0.0, description='Fase (rad):')
    duty = widgets.FloatText(value=0.5, description='Duty cycle:')


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
        




'''
def aplicar_operacoes(series_ativas, operacoes):
    # Verifica se existem pelo menos duas séries ativas
    if len(series_ativas) < 2:
        print('Pelo menos duas séries precisam estar ativas para efetuar as operações')
        return None
    serie_resultante = series_ativas[0]
    
    # Verifica se o número de operações é compatível com o número de séries
    if len(operacoes) != len(series_ativas) - 1:
        print('O número de operações deve ser exatamente um a menos que o número de séries ativas.')
        return None
        
    for i, operacao in enumerate(operacoes):
       
'''