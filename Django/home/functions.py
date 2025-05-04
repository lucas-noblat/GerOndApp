# Bibliotecas utilizadas

from scipy.signal import square, sawtooth
from numpy import linspace, sin, pi, random, abs, fft, array


# Bokeh

from bokeh.plotting import figure, show # Para criar a figure e mostra-la
from bokeh.io import output_notebook, curdoc  # Para exibir no Jupyter Notebook
from bokeh.models import ColumnDataSource # Para atualizar em tempo real
from bokeh.palettes import Category10  # Paleta de cores para os sinais
import warnings


# DEFINIÇÃO DA TAXA DE AMOSTRAGEM QUE SERÁ UTILIZADA EM NOSSO SISTEMA
taxaAmostragem = 1000 #Hz/s

'''FUNÇÕES DE VISUALIZAÇÃO (PLOTAGEM) '''

'''- Matplotlib(Apenas para criação de notebooks)'''


# FUNÇÃO PARA PLOTAR 1 SÉRIE EM GRÁFICO

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10
import warnings

def plotar_sinais_bokeh(
                        x_label="Tempo (s)", 
                        y_label="Amplitude",
                        alpha=1, 
                        cor_grafico="white",
                        tamanho_fonte=16,
                        is_spectrum = False):
    """
    Plota até 6 sinais em um único gráfico usando a biblioteca Bokeh com ColumnDataSource.
    """

    # Cria figura
    p = figure(
        name = "Frequencia" if is_spectrum else "Tempo",
        x_axis_label=x_label,
        y_axis_label=y_label,
        sizing_mode="stretch_both",
        tools="pan,box_zoom,wheel_zoom,reset,save"
    )
    p.toolbar.active_drag = p.tools[0]

    # Cores
    cores = Category10[6]
    
    # Lista para guardar os ColumnDataSources
    sources = []
    sourcesFreq = []

    # Plota cada sinal com ColumnDataSource
    for i in range(6):

        # Cria um ColumnDataSource para esse sinal
        legenda = f'Sinal {i+1}' if i < 5 else 'Resultante'

        if(is_spectrum):
            source = ColumnDataSource(data={'x': [], 'y': []}, name = "dbf" + f"{i}")
            sourcesFreq.append(source)
            print(source.name)
        else:
            source = ColumnDataSource(data={'x': [], 'y': []}, name = "databaseInternoBokeh" + f"{i}")
            sources.append(source)

        
        p.line('x', 'y', source=source, line_width=2, legend_label=legenda,
               line_color=cores[i], line_alpha=alpha)
        

    # Fontes
    font_size = str(tamanho_fonte) + 'pt'
    p.xaxis.major_label_text_font_size = font_size
    p.yaxis.major_label_text_font_size = font_size
    p.xaxis.axis_label_text_font_size = font_size
    p.yaxis.axis_label_text_font_size = font_size

    # Cor de fundo e borda
    p.background_fill_color = cor_grafico
    p.border_fill_color = cor_grafico

    if cor_grafico == "white":
        cor = "black"
    elif cor_grafico == "black":
        cor = "white"
    else:
        cor = "black"

    p.xaxis.axis_label_text_color = cor
    p.yaxis.axis_label_text_color = cor
    p.legend.background_fill_color = cor_grafico
    p.legend.label_text_color = cor
    p.xaxis.major_label_text_color = cor
    p.yaxis.major_label_text_color = cor
    

    # Legenda
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    # Adiciona a figura ao objeto correspondente a sessão bokeh nesse momento

    

    # Retorna a figura e os sources para uso externo
    return p, sourcesFreq if is_spectrum else sources

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
    vetor_tempo = linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False)

    # Sinal gerado
    s = array(amplitude * sin(2 * pi * frequencia * vetor_tempo + fase) + offset)

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

    vetor_tempo = linspace(0, duracao, int(duracao*taxa_amostragem))
    triangular = array(amplitude * sawtooth (2*pi*frequencia*vetor_tempo + fase, duty) + offset)

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
    vetor_tempo = linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False)

    # Gera o sinal quadrado usando scipy.signal.square
    sinal_quadrado = array(amplitude * square(2 * pi * frequencia * vetor_tempo + fase, duty=duty) + offset)

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
    vetor_tempo = linspace(0, duracao, num_componentes, endpoint=False)

    # Gera o ruído branco
    ruido = array(amplitude * random.normal(0, 1, num_componentes) + offset)

    return vetor_tempo, ruido


def gerar_sinal(parametros):


        # Gerando o sinal conforme o tipo inserido

        match parametros['forma_sinal']:
            case "senoidal": 
                vetor_tempo, sinal = sinal_senoidal(amplitude=parametros['amplitude'], 
                                                    frequencia=parametros['frequencia'], 
                                                    duracao=parametros['duracao'],
                                                    offset=parametros['offset'],
                                                    fase=parametros['fase'],
                                                    taxa_amostragem=parametros['rate'])
            case "quadrada":
                vetor_tempo, sinal = sinal_quadrado(amplitude=parametros['amplitude'], 
                                                    frequencia=parametros['frequencia'], 
                                                    duracao=parametros['duracao'], 
                                                    fase=parametros['fase'],
                                                    offset=parametros['offset'],
                                                    duty=parametros['duty'],
                                                    taxa_amostragem=parametros['rate'])
                                                    
            case "triangular":
                vetor_tempo, sinal = sinal_triangular(amplitude=parametros['amplitude'], 
                                                      frequencia=parametros['frequencia'], 
                                                      duracao=parametros['duracao'], 
                                                      fase=parametros['fase'], 
                                                      offset=parametros['offset'],
                                                      taxa_amostragem=parametros['rate'], 
                                                      duty = parametros['duty'])
            case "ruido-branco":
                num_componentes = int(parametros['rate'] * parametros['duracao'])
                vetor_tempo, sinal = ruido_branco(amplitude=parametros['amplitude'], 
                                                  num_componentes=num_componentes , 
                                                  duracao=parametros['duracao'], 
                                                  offset=parametros['offset'])
        return vetor_tempo, sinal


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
    
    # Descobrindo a quantidade de amostras do sinal
    num_amostras = len(sinal)

    # Descobrindo o intervalo de amostragem para ser utilizado
    delta_t = vetor_tempo[1] - vetor_tempo[0]

    # Aplicando a transformada de fourier no sinal de entrada
    fft_sinal = fft.fft(sinal)

    # Definindo o vetor de frequências
    freqs = fft.fftfreq(num_amostras, d=delta_t)

    # Utilizando uma mascara para filtrar os valores positivos da frequência (pois os negativos não importam para nós)
    mascara = freqs >= 0
    freqs_positivas = freqs[mascara]
    fft_sinal_positivo = fft_sinal[mascara]

    if retornar_magnitude:
        return freqs_positivas, abs(fft_sinal_positivo)
    else:
        return freqs_positivas, fft_sinal_positivo
    
    '''
    Pegamos apenas os valores positivos de frequência pois os negativos são apenas um artefato que surge devido a natureza complexa da 
    transformada. No mundo real não faz sentido falar sobre uma onda que possui frequência negativa.

    Porém, o uso da função abs() discarta a informação da fase do sinal, por isso se o usuário desejar saber sobre a fase
    do sinal, deverá desativar o parâmetro 'retornar_magnitude' 
    '''



#FUNÇÃO PARA GERAR SINAIS