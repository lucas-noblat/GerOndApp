# Bibliotecas utilizadas


import numpy as np
import matplotlib.pyplot as plt

import scipy as scp
from ipywidgets import widgets, interact
from scipy.signal import square


# Bokeh

from bokeh.plotting import figure, show # Para criar a figure e mostra-la
from bokeh.io import output_notebook  # Para exibir no Jupyter Notebook
from bokeh.models import ColumnDataSource # Para atualizar em tempo real
from bokeh.palettes import Category10  # Paleta de cores para os sinais
import warnings


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


'''BOKEH'''

from bokeh.plotting import figure, show
from bokeh.io import output_notebook  # Para exibir no Jupyter Notebook
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10  # Paleta de cores para os sinais
import warnings


def plotar_sinais_bokeh(vetor_x, lista_vetores_y, titulo="Sinais", x_label="Tempo (s)", y_label="Amplitude", largura=1280, altura=400, is_spectrum=False):
    """
    Plota até 6 sinais em um único gráfico usando a biblioteca Bokeh.

    Parâmetros:
    vetor_x: Vetor de valores para o eixo x (tempo ou frequência).
    lista_vetores_y: Lista de vetores de valores para o eixo y (amplitude ou magnitude).
    titulo: Título do gráfico.
    x_label: Rótulo do eixo x.
    y_label: Rótulo do eixo y.
    largura: Largura do gráfico em pixels (padrão: 1280).
    altura: Altura do gráfico em pixels (padrão: 400).
    is_spectrum: Se True, ajusta os limites do eixo x usando o Teorema de Nyquist.
    """
    # Configura o ambiente do Bokeh (opcional, apenas para Jupyter Notebook)
    output_notebook()

    # Verifica se há mais de 6 sinais
    if len(lista_vetores_y) > 6:
        warnings.warn("A função suporta no máximo 6 sinais. Apenas os primeiros 6 serão plotados.")
        lista_vetores_y = lista_vetores_y[:6]  # Limita a lista aos primeiros 6 sinais

    # Calcula os limites dos eixos x e y com base nos dados
    x_min = min(vetor_x)  # Valor mínimo do eixo x
    x_max = max(vetor_x)  # Valor máximo do eixo x

    # Encontra os valores mínimo e máximo de todos os sinais no eixo y
    y_min = min([min(y) for y in lista_vetores_y])  # Valor mínimo do eixo y
    y_max = max([max(y) for y in lista_vetores_y])  # Valor máximo do eixo y

    # Adiciona uma margem de 10% aos limites para melhor visualização
    margem_x = (x_max - x_min) * 0.1
    margem_y = (y_max - y_min) * 0.1

    x_min_ajustado = x_min - margem_x
    x_max_ajustado = x_max + margem_x
    y_min_ajustado = y_min - margem_y
    y_max_ajustado = y_max + margem_y


    # Cria a figura do Bokeh com os limites ajustados
    p = figure(
        title=titulo,
        x_axis_label=x_label,
        y_axis_label=y_label,
        width=largura,
        height=altura,
        tools="pan,box_zoom,wheel_zoom,reset,save",
        x_range=(x_min_ajustado, x_max_ajustado),  # Limites ajustados do eixo x
        y_range=(y_min_ajustado, y_max_ajustado)   # Limites ajustados do eixo y
    )

    # Paleta de cores para os sinais (6 cores)
    cores = Category10[6]

    # Plota cada sinal
    for i, vetor_y in enumerate(lista_vetores_y):
        # Cria um ColumnDataSource para armazenar os dados
        fonte = ColumnDataSource(data={'x': vetor_x, 'y': vetor_y})

        # Adiciona a linha ao gráfico com uma cor da paleta
        p.line('x', 'y', source=fonte, line_width=2, line_color=cores[i], legend=f"Sinal {i+1}")

    # Configura a legenda
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"  # Permite ocultar as linhas ao clicar na legenda

    # Exibe o gráfico
    show(p)

''' FUNÇÕES MATEMÁTICAS PARA CRIAR OS SINAIS '''

# Onda Senoidal

def sinal_senoidal(amplitude, frequencia, taxa_amostragem=1000, duracao=1, fase=0, offset=0):
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


# TRANSFORMADA DE FOURIER

def transformada_fourier(vetor_tempo, sinal, retornar_magnitude=True):
    """
    Transforma um sinal do domínio do tempo para o domínio da frequência.

    Parâmetros:
    vetor_tempo: Vetor de tempo correspondente ao sinal.
    sinal: Sinal no domínio do tempo.
    retornar_magnitude: Se True, retorna a magnitude. Se False, retorna os valores complexos.

    Retorna:
    freqs: Vetor de frequências correspondente à Transformada de Fourier (apenas positivas).
    fft_resultado: Magnitude ou valores complexos da Transformada de Fourier.
    """
    num_amostras = len(sinal)
    delta_t = vetor_tempo[1] - vetor_tempo[0]
    fft_sinal = np.fft.fft(sinal)
    freqs = np.fft.fftfreq(num_amostras, d=delta_t)
    mascara = freqs >= 0
    freqs_positivas = freqs[mascara]
    fft_sinal_positivo = fft_sinal[mascara]

    if retornar_magnitude:
        return freqs_positivas, np.abs(fft_sinal_positivo)
    else:
        return freqs_positivas, fft_sinal_positivo
    
    '''
    Pegamos apenas os valores positivos de frequência pois os negativos são apenas um artefato que surge devido a natureza complexa da 
    transformada. No mundo real não faz sentido falar sobre uma onda que possui frequência negativa.

    Porém, o uso da função abs() discarta a informação da fase do sinal, por isso se o usuário desejar saber sobre a fase
    do sinal, deverá desativar o parâmetro 'retornar_magnitude' 
    '''



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
